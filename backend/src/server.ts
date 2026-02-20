import { recoverStuckIngestions } from "./services/ingestionRecovery.service";
// src/server.ts

/* -------------------------------------------------------------------------- */
/*                               ENV (MUST BE FIRST)                          */
/* -------------------------------------------------------------------------- */
import dotenv from "dotenv";

dotenv.config({
  path: process.env.NODE_ENV === "production"
    ? ".env.production"
    : ".env",
});

/* -------------------------------------------------------------------------- */
/*                                Imports                                     */
/* -------------------------------------------------------------------------- */
import helmet from "helmet";
import { apiLimiter } from "./middleware/rateLimit.middleware";
import express from "express";
import cookieParser from "cookie-parser";
import morgan from "morgan";

import { connectDB } from "./config/db";

// Routes
import authRoutes from "./routes/auth.routes";
import judgmentRoutes from "./routes/judgment.routes";
import ingestionRoutes from "./routes/ingestion.routes";
import nlpRoutes from "./routes/nlp.routes";
import locationRoutes from "./routes/location.routes";
import pricingRoutes from "./routes/pricing.routes";
import superadminRoutes from "./routes/superadmin";
import superadminUploadRoutes from "./routes/superadmin/upload.routes";
import adminRoutes from "./routes/admin.routes";

/* -------------------------------------------------------------------------- */
/*                               Server Bootstrap                              */
/* -------------------------------------------------------------------------- */
async function startServer() {
  try {
    await connectDB();
  await recoverStuckIngestions();

setInterval(async () => {
  try {
    console.log("🔁 Periodic ingestion recovery check...");
    await recoverStuckIngestions();
  } catch (err) {
    console.error("❌ Recovery watchdog error:", err);
  }
}, 5 * 60 * 1000);

    const app = express();
app.set("trust proxy", 1);

    /* ---------------------------- Middleware -------------------------------- */

    app.use(express.json({ limit: "1gb" }));
    app.use(helmet());
    app.use("/api", apiLimiter);    

    app.use(express.urlencoded({ extended: true, limit: "1gb" }));
    app.use(cookieParser());
    app.use(morgan("dev"));

    /* ------------------------------- Routes --------------------------------- */

    // Health (no auth, no dependencies)
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
        service: "solvelitigation-backend",
        uptime: process.uptime(),
      });
    });

    // Auth & core APIs
    app.use("/api/auth", authRoutes);
    app.use("/api/judgments", judgmentRoutes);
    app.use("/api/ingestions", ingestionRoutes);
    app.use("/api/nlp", nlpRoutes);
    app.use("/api/location", locationRoutes);
    app.use("/api/pricing", pricingRoutes);
    app.use("/api/admin", adminRoutes);
    
// Superadmin
    app.use("/api/superadmin", superadminRoutes);
    app.use("/api/superadmin", superadminUploadRoutes);

    /* ---------------------------- 404 Handler ------------------------------- */

    app.use((_req, res) => {
      res.status(404).json({
        success: false,
        message: "API route not found",
      });
    });

    /* ------------------------- Global Error Handler -------------------------- */
    // ❗ MUST be AFTER all routes
    app.use(
      (
        err: any,
        _req: express.Request,
        res: express.Response,
        _next: express.NextFunction
      ) => {
        console.error("🔥 GLOBAL ERROR HANDLER 🔥");
        console.error(err);

        // Multer
        if (err?.code === "LIMIT_FILE_SIZE") {
          return res.status(400).json({ message: "File too large" });
        }

        // Mongoose
        if (err?.name === "CastError") {
          return res.status(400).json({ message: "Invalid ID format" });
        }

        return res.status(err?.status || 500).json({
          message: err?.message || "Internal Server Error",
        });
      }
    );

    /* ------------------------------ Listen ---------------------------------- */

const PORT = Number(process.env.PORT) || 4000;

const server = app.listen(PORT, "127.0.0.1", () => {
  console.log(`🚀 Server running on port ${PORT}`);
});

/* --------------------- Graceful Shutdown --------------------- */

const shutdown = async (signal: string) => {
  console.log(`🛑 ${signal} received. Shutting down gracefully...`);

  server.close(async () => {
    console.log("🔌 HTTP server closed");

    try {
      const mongoose = await import("mongoose");
      await mongoose.default.connection.close();
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
