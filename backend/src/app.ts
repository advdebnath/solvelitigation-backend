import express from "express";
import cors from "cors";
import cookieParser from "cookie-parser";

// Routes
import authRoutes from "./routes/auth.routes";
import judgmentRoutes from "./routes/judgment.routes";
import healthRoute from "./routes/health.route";

// Config

const FRONTEND_URL = process.env.FRONTEND_URL;

const app = express();

/* -------------------------------------------------------------------------- */
/*                               Global Middleware                             */
/* -------------------------------------------------------------------------- */

app.use(
  cors({
    origin: FRONTEND_URL,
    credentials: true,
  })
);

app.use(express.json({ limit: "20mb" }));
app.use(express.urlencoded({ extended: true }));
app.use(cookieParser());

/* -------------------------------------------------------------------------- */
/*                                   Routes                                   */
/* -------------------------------------------------------------------------- */

// Health must be FIRST (no auth, no side effects)
app.use("/api", healthRoute);

// Auth
app.use("/api/auth", authRoutes);

// Core APIs
app.use("/api/judgments", judgmentRoutes);

/* -------------------------------------------------------------------------- */
/*                              404 Fallback                                  */
/* -------------------------------------------------------------------------- */

app.use((_req, res) => {
  res.status(404).json({
    success: false,
    message: "API route not found",
  });
});

/* -------------------------------------------------------------------------- */
/*                            Global Error Handler                              */
/* -------------------------------------------------------------------------- */

app.use(
  (
    err: any,
    _req: express.Request,
    res: express.Response,
    _next: express.NextFunction
  ) => {
    console.error("🔥 Unhandled Error:", err);

    res.status(err.status || 500).json({
      success: false,
      message: err.message || "Internal Server Error",
    });
  }
);

export default app;
