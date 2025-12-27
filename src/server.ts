import express from "express";
import http from "http";
import cors from "cors";
import cookieParser from "cookie-parser";
import helmet from "helmet";
import morgan from "morgan";
import mongoose from "mongoose";

// ROUTES (RELATIVE IMPORTS ONLY)
import authRoutes from "./routes/auth.routes";
import healthRoutes from "./routes/health.routes";
import judgmentRoutes from "./routes/judgments/judgments.routes";
import actRoutes from "./routes/acts.routes";
import superadminJudgmentUploadRoutes from "./routes/superadmin/judgment.upload.routes";
import superadminRoutes from "./routes/superadmin";
import jobRoutes from "./routes/job.routes";

import { processJobsSerially } from "@/workers/job.worker";
// -------------------- APP --------------------
const app = express();
app.set("trust proxy", 1);
const server = http.createServer(app);
// -------------------- MIDDLEWARES --------------------
app.use(cors());
app.use(express.json({ limit: "20mb" }));  // JSON payloads only
app.use(express.urlencoded({ extended: true, limit: "20mb" }));
// IMPORTANT: allow large multipart uploads (handled by multer)
app.set("maxFileSize", 900 * 1024 * 1024); // 900MB
app.use(cookieParser());
app.use(helmet());
app.use(morgan("dev"));
// -------------------- DATABASE --------------------
const MONGO_URI =
  process.env.MONGO_URI || "mongodb://127.0.0.1:27017/solvelitigation";
mongoose
  .connect(MONGO_URI)
  .then(() => console.log("✅ MongoDB connected"))
  .catch((err) =>
    console.error("❌ MongoDB connection error:", err)
  );
// -------------------- ROUTES --------------------

// 🔁 Background job worker (Phase 2)
setInterval(() => {
  processJobsSerially().catch(err => console.error("[JOB_WORKER]", err));
}, 1000);

app.use("/api/health", healthRoutes);
app.use("/api/auth", authRoutes);
app.use("/api/judgments", judgmentRoutes);
app.use("/api/acts", actRoutes);
app.use("/api/superadmin/judgments", superadminJudgmentUploadRoutes);
app.use("/api/superadmin", superadminRoutes);
app.use("/api/jobs", jobRoutes);
// -------------------- START SERVER --------------------
const PORT = Number(process.env.PORT) || 4000;
server.listen(PORT, "0.0.0.0", () => {
  console.log(`[boot] server listening on http://0.0.0.0:${PORT}`);
});
