import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

/* ---------------- ROUTES ---------------- */
import authRoutes from "./routes/auth.routes";
import judgmentRoutes from "./routes/judgment.routes";
import searchRoutes from "./routes/search.routes";
import similarRoutes from "./routes/similar.routes";
import ingestionRoutes from "./routes/ingestion.routes";
import healthRoute from "./routes/health.route";
import explorerRoutes from "./routes/explorer.routes";
import aiRoutes from "./routes/ai.routes";
import suggestRoutes from "./routes/suggest.routes";
import adminRoutes from "./routes/admin.routes";
import textLiquidRoutes from "./routes/textLiquid.routes";
import studentRoutes from "./routes/student.routes";
import reviewRoutes from "./routes/review.routes";
import draftRoutes from "./routes/draft.routes";
import bundleRoutes from "./routes/bundle.routes";
import pipelineRoutes from "./routes/pipeline.routes";
import judgmentViewRoutes from "./routes/judgment.view.routes";
import caseHistoryRoutes from "./routes/caseHistory.routes";
import actRoutes from "./routes/acts.routes";

/* ---------------- 🔥 AUTH MIDDLEWARE ---------------- */
import auth from "./middleware/auth.middleware"
/* ---------------- CONFIG ---------------- */
const FRONTEND_URL = process.env.FRONTEND_URL || "*";

const app = express();

/* -------------------------------------------------------------------------- */
/*                               GLOBAL MIDDLEWARE                            */
/* -------------------------------------------------------------------------- */

app.use(
  cors({
    origin: FRONTEND_URL,
    credentials: true,
  })
);

app.use(express.json({ limit: "50mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

/* -------------------------------------------------------------------------- */
/*                               SAFE DEBUG LOGGER                            */
/* -------------------------------------------------------------------------- */

if (process.env.NODE_ENV !== "production") {
  app.use((req, _res, next) => {
    console.log(`➡ ${req.method} ${req.originalUrl}`);
    next();
  });
}

/* -------------------------------------------------------------------------- */
/*                           BASE & HEALTH ROUTES                             */
/* -------------------------------------------------------------------------- */

// ✅ Base route (quick test)
app.get("/", (_req, res) => {
  res.send("SolveLitigation Backend Running");
});

// ✅ Direct health fallback (never fails)
app.get("/api/health-check", (_req, res) => {
  res.json({
    success: true,
    status: "ok",
    time: new Date()
  });
});

// ✅ Main health route
app.use("/api/health", healthRoute);

/* -------------------------------------------------------------------------- */
/*                                   ROUTES                                   */
/* -------------------------------------------------------------------------- */

// Public
app.use("/api/auth", authRoutes);

// Core
app.use("/api/judgments", judgmentRoutes);
app.use("/api/search", searchRoutes);
app.use("/api/similar", similarRoutes);

// Explorer + AI (IMPORTANT ORDER)
app.use("/api/explorer", explorerRoutes);
app.use("/api/ai", aiRoutes);

// Additional
app.use("/api/suggest", suggestRoutes);
app.use("/api/review", auth, reviewRoutes);
app.use("/api/drafts", draftRoutes);
app.use("/api/bundle", bundleRoutes);
app.use("/api/pipeline", pipelineRoutes);
app.use("/api/judgment", judgmentViewRoutes);
app.use("/api/case-history", caseHistoryRoutes);
app.use("/api/acts", actRoutes);
app.use("/api/review", reviewRoutes);

// Secured
app.use("/api/student", auth, studentRoutes);

// Utilities
app.use("/api/text-liquid", textLiquidRoutes);
app.use("/api/ingestions", ingestionRoutes);
app.use("/api/admin", adminRoutes);

/* -------------------------------------------------------------------------- */
/*                              404 FALLBACK                                  */
/* -------------------------------------------------------------------------- */

app.use((_req, res) => {
  res.status(404).json({
    success: false,
    message: "API route not found",
  });
});

/* -------------------------------------------------------------------------- */
/*                            GLOBAL ERROR HANDLER                            */
/* -------------------------------------------------------------------------- */

app.use((err: any, _req: express.Request, res: express.Response, _next: express.NextFunction) => {
  console.error("🔥 Unhandled Error:", err);

  res.status(err.status || 500).json({
    success: false,
    message: err.message || "Internal Server Error",
  });
});

export default app;
