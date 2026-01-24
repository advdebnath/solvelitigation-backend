import express from "express";
import cors from "cors";
import morgan from "morgan";
import cookieParser from "cookie-parser";

import authRoutes from "@/routes/auth.routes";
import judgmentRoutes from "@/routes/judgments/judgments.routes";
import nlpRoutes from "@/routes/nlp.routes";

const PORT = process.env.PORT || 4000;

function createServer() {
  const app = express();

  // Middleware
  app.use(cors({ origin: true, credentials: true }));
  app.use(express.json({ limit: "50mb" }));
  app.use(express.urlencoded({ extended: true }));
  app.use(cookieParser());
  app.use(morgan("dev"));

  // Routes
  app.use("/api/auth", authRoutes);
  app.use("/api/judgments", judgmentRoutes);
  app.use("/api/nlp", nlpRoutes);

  // Health check
  app.get("/health", (_req, res) => {
    res.status(200).json({ status: "ok" });
  });

  // Fallback
  app.use((_req, res) => {
    res.status(404).json({ error: "Not Found" });
  });

  return app;
}

const app = createServer();

app.listen(PORT, () => {
  console.log(`🚀 Backend running on port ${PORT}`);
});
