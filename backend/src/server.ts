// src/server.ts

import dotenv from "dotenv";

// 🔴 MUST be FIRST — before any other import
dotenv.config({
  path: process.env.NODE_ENV === "production"
    ? ".env.production"
    : ".env",
});

// ------------------
// All other imports BELOW
// ------------------

import express from "express";
import cookieParser from "cookie-parser";
import morgan from "morgan";
import mongoose from "mongoose";

import authRoutes from "./routes/auth.routes";
import judgmentRoutes from "./routes/judgment.routes";
import nlpRoutes from "./routes/nlp.routes";
import locationRoutes from "./routes/location.routes";
import pricingRoutes from "./routes/pricing.routes";
import superadminRoutes from "./routes/superadmin";
import superadminUploadRoutes from "./routes/superadmin/upload.routes";
import { connectDB } from "./config/db";

async function startServer() {
  try {
    console.log("⏳ Connecting to MongoDB...");
    await connectDB();

    const app = express();

    app.use(express.json({ limit: "1gb" }));
    app.use(express.urlencoded({ extended: true, limit: "1gb" }));
    app.use(cookieParser());
    app.use(morgan("dev"));

    app.use("/api/auth", authRoutes);
    app.use("/api/judgments", judgmentRoutes);
    app.use("/api/nlp", nlpRoutes);
    app.use("/api/location", locationRoutes);
    app.use("/api/pricing", pricingRoutes);
    app.use("/api/superadmin", superadminRoutes);
    app.use("/api/superadmin", superadminUploadRoutes);
    app.get("/health", (_req, res) => {
      res.json({ status: "OK" });
    });

    const PORT = process.env.PORT || 4000;

    app.get("/api/healthz", (_req, res) => {
      res.status(200).json({
        status: "OK",
        service: "solvelitigation-backend",
        time: new Date().toISOString(),
      });
    });

    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
    });
  } catch (err) {
    console.error("❌ Server failed to start", err);
    process.exit(1);
  }
}

startServer();
