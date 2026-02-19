import { Request, Response } from "express";
import mongoose from "mongoose";
import axios from "axios";

let Redis: any = null;

// Lazy load Redis safely
try {
  Redis = require("ioredis");
} catch {
  console.warn("⚠ Redis module not available — skipping Redis health check");
}

export const getSystemHealth = async (req: Request, res: Response) => {
  let mongoStatus = "DOWN";
  let redisStatus = "DOWN";
  let nlpStatus = "DOWN";

  // Mongo check
  try {
    if (mongoose.connection.readyState === 1) {
      mongoStatus = "UP";
    }
  } catch {
    mongoStatus = "DOWN";
  }

  // Redis check (only if module available)
  if (Redis) {
    try {
      const redis = new Redis(process.env.REDIS_URL || "redis://127.0.0.1:6379");
      await redis.ping();
      redisStatus = "UP";
      redis.disconnect();
    } catch {
      redisStatus = "DOWN";
    }
  }

  // NLP check (optional — adjust URL if needed)
  try {
    await axios.get(process.env.NLP_HEALTH_URL || "http://127.0.0.1:8000/health");
    nlpStatus = "UP";
  } catch {
    nlpStatus = "DOWN";
  }

  const overall =
    mongoStatus === "UP" &&
    redisStatus === "UP" &&
    nlpStatus === "UP"
      ? "HEALTHY"
      : "DEGRADED";

  res.json({
    success: true,
    data: {
      mongo: mongoStatus,
      redis: redisStatus,
      nlp: nlpStatus,
      status: overall,
    },
  });
};
