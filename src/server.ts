import "dotenv/config";
import express from "express";
import http from "http";
import cors from "cors";
import cookieParser from "cookie-parser";
import helmet from "helmet";
import morgan from "morgan";
import mongoose from "mongoose";


import cfg from "@/config";

import { startCleanupUnverifiedUsersJob } from "@/jobs/cleanupUnverifiedUsers.job";

// ROUTES
import authRoutes from "./routes/auth.routes";
import healthRoutes from "./routes/health.routes";
import judgmentRoutes from "./routes/judgments/judgments.routes";
import actRoutes from "./routes/acts.routes";
import superadminRoutes from "./routes/superadmin";
import superadminUsersRoutes from "@/routes/superadmin/users.routes";
import jobRoutes from "./routes/job.routes";
import pricingRoutes from "./routes/pricing.routes";
import locationRoutes from "./routes/location.routes";
import nlpRoutes from "./routes/nlp.routes";
import { planExpiryJob } from "@/jobs/planExpiry.job";

// JOB WORKER
import { processJobsSerially } from "./workers/job.worker";

const app = express();
app.set("trust proxy", 1);

const server = http.createServer(app);

/* --------------------------------------------------
   MIDDLEWARES
-------------------------------------------------- */

// CORS — MUST be before routes
app.use(
  cors({
    origin: [
      "https://solvelitigation.com",
      "https://www.solvelitigation.com",
    ],
    credentials: true, // ✅ REQUIRED for HttpOnly auth cookies
  })
);

app.use(express.json({ limit: "900mb" }));
app.use(express.urlencoded({ extended: true, limit: "900mb" }));
app.set("maxFileSize", 900 * 1024 * 1024);

app.use(cookieParser());
app.use(helmet());
app.use(morgan("dev"));


/* --------------------------------------------------
   DATABASE
-------------------------------------------------- */
const MONGO_URI =
  process.env.MONGO_URI || "mongodb://127.0.0.1:27017/solvelitigation";


mongoose
  .connect(MONGO_URI)
  .then(() => {
    console.log("✅ MongoDB connected");
planExpiryJob();





// ✅ Start cron job ONCE
    startCleanupUnverifiedUsersJob();
  })

  .catch((err) => {
    console.error("❌ MongoDB connection failed", err);
  });



/* --------------------------------------------------
   BACKGROUND JOB WORKER
-------------------------------------------------- */

setInterval(() => {
  processJobsSerially().catch((err) =>
    console.error("[JOB_WORKER]", err)
  );
}, 1000);

/* --------------------------------------------------
   ROUTES
-------------------------------------------------- */

app.use("/api/health", healthRoutes);
app.use("/api/auth", authRoutes);
app.use("/api/judgments", judgmentRoutes);
app.use("/api/nlp", nlpRoutes);
app.use("/api/acts", actRoutes);
app.use("/api/superadmin", superadminRoutes);
app.use("/api/superadmin", superadminUsersRoutes);
app.use("/api/jobs", jobRoutes);
app.use("/api/pricing", pricingRoutes);
app.use("/api/location", locationRoutes);


/* --------------------------------------------------
   START SERVER
-------------------------------------------------- */

const PORT = Number(process.env.PORT) || 4000;

(async () => {
  try {


    console.log("✅ MongoDB connected");

    // 🔁 Start cron jobs AFTER DB is ready
    startCleanupUnverifiedUsersJob();

    app.listen(PORT, () => {
      console.log(`🚀 Server running on port ${PORT}`);
    });
  } catch (err) {
    console.error("❌ Server startup failed:", err);
    process.exit(1);
  }
})();





