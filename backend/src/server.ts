// src/server.ts

/* -----------------------------------------------------------
   ENV (MUST BE FIRST)
------------------------------------------------------------ */
import dotenv from "dotenv";

dotenv.config({
  path:
    process.env.NODE_ENV === "production"
      ? ".env.production"
      : ".env",
});

/* -----------------------------------------------------------
   Imports
------------------------------------------------------------ */
import express from "express";
import helmet from "helmet";
import cookieParser from "cookie-parser";
import morgan from "morgan";
import http from "http";
import mongoose from "mongoose";
import { Server as SocketIOServer } from "socket.io";

import { apiLimiter } from "./middleware/rateLimit.middleware";
import { requestLogger } from "./middleware/requestLogger.middleware";
import { connectDB } from "./config/db";
import { connectRedis } from "./config/redis";
import { recoverStuckIngestions } from "./services/ingestionRecovery.service";

// Routes
import authRoutes from "./routes/auth.routes";
import judgmentRoutes from "./routes/judgment.routes";
import ingestionRoutes from "./routes/ingestion.routes";
import nlpRoutes from "./routes/nlp.routes";
import locationRoutes from "./routes/location.routes";
import pricingRoutes from "./routes/pricing.routes";
import superadminRoutes from "./routes/superadmin";
import adminRoutes from "./routes/admin.routes";

/* -----------------------------------------------------------
   Exportable IO Instance
------------------------------------------------------------ */
export let io: SocketIOServer;

/* -----------------------------------------------------------
   Server Bootstrap
------------------------------------------------------------ */
async function startServer() {
  try {
    /* ---------------- Database ---------------- */
    await connectDB();
    console.log("✅ Connected to MongoDB");

    /* ---------------- Redis ---------------- */
    await connectRedis();
    console.log("✅ Redis connected");

    /* ---------------- Recovery ---------------- */
    await recoverStuckIngestions();

    setInterval(async () => {
      try {
        console.log("🔁 Periodic ingestion recovery check...");
        await recoverStuckIngestions();
      } catch (err) {
        console.error("❌ Recovery watchdog error:", err);
      }
    }, 5 * 60 * 1000);

    /* ---------------- Express App ---------------- */
    const app = express();
    app.set("trust proxy", 1);

    /* ---------------- Middleware ---------------- */
    app.use(requestLogger);
    app.use(express.json({ limit: "1gb" }));
    app.use(express.urlencoded({ extended: true, limit: "1gb" }));
    app.use(cookieParser());
    app.use(helmet());
    app.use(morgan("dev"));
    app.use("/api", apiLimiter);

    /* ---------------- Health Routes ---------------- */
    app.get("/api/health", (_req, res) => {
      res.status(200).json({
        status: "OK",
        service: "solvelitigation-backend",
        time: new Date().toISOString(),
      });
    });

    app.get("/api/healthz", (_req, res) => {
      res.status(200).json({
        status: "OK",
        uptime: process.uptime(),
      });
    });

    /* ---------------- API Routes ---------------- */
    app.use("/api/auth", authRoutes);
    app.use("/api/judgments", judgmentRoutes);
    app.use("/api/ingestions", ingestionRoutes);
    app.use("/api/nlp", nlpRoutes);
    app.use("/api/location", locationRoutes);
    app.use("/api/pricing", pricingRoutes);
    app.use("/api/admin", adminRoutes);
    app.use("/api/superadmin", superadminRoutes);

    /* ---------------- 404 Handler ---------------- */
    app.use((_req, res) => {
      res.status(404).json({
        success: false,
        message: "API route not found",
      });
    });

    /* ---------------- Global Error Handler ---------------- */
    app.use(
      (
        err: any,
        _req: express.Request,
        res: express.Response,
        _next: express.NextFunction
      ) => {
        console.error("🔥 GLOBAL ERROR HANDLER 🔥", err);

        if (err?.code === "LIMIT_FILE_SIZE") {
          return res.status(400).json({ message: "File too large" });
        }

        if (err?.name === "CastError") {
          return res.status(400).json({ message: "Invalid ID format" });
        }

        return res.status(err?.status || 500).json({
          message: err?.message || "Internal Server Error",
        });
      }
    );

    /* ---------------- HTTP + SOCKET ---------------- */
    const PORT = Number(process.env.PORT) || 4000;
    const httpServer = http.createServer(app);
    httpServer.setTimeout(60000); // 60 seconds request timeout protection

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

httpServer.listen(PORT, "0.0.0.0", () => {
  console.log(`🚀 Server running on port ${PORT}`);
});


    /* ---------------- Graceful Shutdown ---------------- */
    const shutdown = async (signal: string) => {
      console.log(`🛑 ${signal} received. Shutting down gracefully...`);

      httpServer.close(async () => {
        console.log("🔌 HTTP server closed");

        try {
          await mongoose.connection.close();
          console.log("📦 MongoDB connection closed");
        } catch (err) {
          console.error("❌ Error closing MongoDB:", err);
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

/* ---------------- Process Safety Guards ---------------- */

process.on("unhandledRejection", (reason: any) => {
  console.error("🚨 UNHANDLED REJECTION:", reason);
});

process.on("uncaughtException", (err: Error) => {
  console.error("🚨 UNCAUGHT EXCEPTION:", err);
  process.exit(1); // Let PM2 restart cleanly
});
