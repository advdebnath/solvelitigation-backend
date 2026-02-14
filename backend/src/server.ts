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

/* -------------------------------------------------------------------------- */
/*                               Server Bootstrap                              */
/* -------------------------------------------------------------------------- */
async function startServer() {
  try {
    console.log("⏳ Connecting to MongoDB...");
    await connectDB();
    console.log("✅ Connected to MongoDB");

    const app = express();

    /* ---------------------------- Middleware -------------------------------- */

    app.use(express.json({ limit: "1gb" }));
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

    app.listen(PORT, "127.0.0.1", () => {
      console.log(`🚀 Server running on port ${PORT}`);
    });

  } catch (err) {
    console.error("❌ Server failed to start", err);
    process.exit(1);
  }
}

startServer();
