// src/server.ts

import dotenv from "dotenv";

/* -----------------------------------------------------------
   🔥 LOAD ENV FIRST (CRITICAL)
----------------------------------------------------------- */
dotenv.config({
  path:
    process.env.NODE_ENV === "production"
      ? ".env.production"
      : ".env",
});

/* ----------------------------------------------------------- */
import http from "http";
import mongoose from "mongoose";
import { Server as SocketIOServer } from "socket.io";

import app from "./app";

// 🔥 VERY IMPORTANT (FIX NGINX + RATE LIMIT ISSUE)
app.set("trust proxy", 1);

import { connectDB } from "./config/db";
import { connectRedis } from "./config/redis";
import { recoverStuckIngestions } from "./services/ingestionRecovery.service";

// 🔥 ADD THIS IMPORT (IMPORTANT FIX)
import JudgmentIngestion from "./models/JudgmentIngestion";

/* ----------------------------------------------------------- */
export let io: SocketIOServer;

/* ----------------------------------------------------------- */
async function sanitizeInvalidStages() {
  try {
    console.log("🧹 Sanitizing invalid ingestion stages...");

    const validStages = ["UPLOADED","QUEUED","PROCESSING","COMPLETED","FAILED"];

    const result = await JudgmentIngestion.updateMany(
      { stage: { $nin: validStages } },
      {
        $set: {
          stage: "PROCESSING",
          status: "QUEUED",
          isLocked: false,
          error: null,
        },
      }
    );

    if (result.modifiedCount > 0) {
      console.log(`🧹 Fixed ${result.modifiedCount} invalid stage records`);
    } else {
      console.log("✅ No invalid stages found");
    }

  } catch (err) {
    console.error("❌ Stage sanitization failed:", err);
  }
}

/* ----------------------------------------------------------- */
async function startServer() {
  try {
    /* ---------------- Database ---------------- */
    await connectDB();
    console.log("✅ Connected to MongoDB");

    /* 🔥 CRITICAL FIX: CLEAN INVALID DATA BEFORE ANYTHING */
    await sanitizeInvalidStages();

    /* ---------------- Redis ---------------- */
    await connectRedis();
    console.log("✅ Redis connected");

    /* ---------------- Recovery ---------------- */
    await recoverStuckIngestions();

    setInterval(async () => {
      try {
        console.log("🔁 Periodic ingestion recovery check...");

        // 🔥 ALWAYS SANITIZE BEFORE RECOVERY
        await sanitizeInvalidStages();

        await recoverStuckIngestions();

      } catch (err) {
        console.error("❌ Recovery watchdog error:", err);
      }
    }, 5 * 60 * 1000);

    /* ---------------- HTTP SERVER ---------------- */
    const PORT = Number(process.env.PORT) || 4000;
    const httpServer = http.createServer(app);

    httpServer.setTimeout(60000);

    /* ---------------- SOCKET ---------------- */
    io = new SocketIOServer(httpServer, {
      cors: {
        origin: process.env.FRONTEND_URL || "*",
        credentials: true,
      },
    });

    io.on("connection", (socket) => {
      console.log("🔌 Client connected:", socket.id);

      socket.on("disconnect", () => {
        console.log("❌ Client disconnected:", socket.id);
      });
    });

    /* ---------------- START ---------------- */
    httpServer.listen(PORT, "0.0.0.0", () => {
      console.log(`🚀 Server running on port ${PORT}`);
    });

    /* ---------------- SHUTDOWN ---------------- */
    const shutdown = async (signal: string) => {
      console.log(`🛑 ${signal} received. Shutting down...`);

      httpServer.close(async () => {
        console.log("🔌 HTTP server closed");

        try {
          await mongoose.connection.close();
          console.log("📦 MongoDB closed");
        } catch (err) {
          console.error("❌ Mongo close error:", err);
        }

        process.exit(0);
      });
    };

    process.on("SIGTERM", () => shutdown("SIGTERM"));
    process.on("SIGINT", () => shutdown("SIGINT"));

  } catch (err) {
    console.error("❌ Server failed to start", err);
    process.exit(1);
  }
}

startServer();

/* ---------------- PROCESS SAFETY ---------------- */

process.on("unhandledRejection", (reason: any) => {
  console.error("🚨 UNHANDLED REJECTION:", reason);
});

process.on("uncaughtException", (err: Error) => {
  console.error("🚨 UNCAUGHT EXCEPTION:", err);
  process.exit(1);
});
