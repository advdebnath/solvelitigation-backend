import { Request, Response } from "express";
import os from "os";
import mongoose from "mongoose";
import Judgment from "../../models/judgment.model";
import JudgmentIngestion from "../../models/JudgmentIngestion";
import { redisClient } from "../../config/redis";

const CACHE_KEY = "admin:system-stats";
const CACHE_TTL = 15; // seconds

export const getSystemStats = async (_req: Request, res: Response) => {
  try {
    /* ---------------------------
       Check Redis Cache
    ---------------------------- */
    if (redisClient?.isOpen) {
      const cached = await redisClient.get(CACHE_KEY);
      if (cached) {
        return res.status(200).json({
          success: true,
          cached: true,
          data: JSON.parse(cached),
        });
      }
    }

    /* ---------------------------
       Compute Stats
    ---------------------------- */
    const [
      totalJudgments,
      totalIngestions,
      nlpCompleted,
      ingestionQueued,
      ingestionProcessing,
      ingestionCompleted,
      ingestionFailed,
      ingestionPermanentFailure,
    ] = await Promise.all([
      Judgment.countDocuments(),
      JudgmentIngestion.countDocuments(),
      Judgment.countDocuments({ nlpStatus: "COMPLETED" }),
      JudgmentIngestion.countDocuments({ status: "QUEUED" }),
      JudgmentIngestion.countDocuments({ status: "PROCESSING" }),
      JudgmentIngestion.countDocuments({ status: "COMPLETED" }),
      JudgmentIngestion.countDocuments({ status: "FAILED" }),
      JudgmentIngestion.countDocuments({ status: "PERMANENT_FAILURE" }),
    ]);

    const memoryUsage = process.memoryUsage();

    const stats = {
      database: {
        mongoConnected: mongoose.connection.readyState === 1,
        totalJudgments,
        totalIngestions,
      },
      nlp: {
        completed: nlpCompleted,
      },
      ingestion: {
        queued: ingestionQueued,
        processing: ingestionProcessing,
        completed: ingestionCompleted,
        failed: ingestionFailed,
        permanentFailure: ingestionPermanentFailure,
      },
      redis: {
        connected: redisClient?.isOpen || false,
      },
      system: {
        uptimeSeconds: process.uptime(),
        memoryMB: {
          rss: (memoryUsage.rss / 1024 / 1024).toFixed(2),
          heapUsed: (memoryUsage.heapUsed / 1024 / 1024).toFixed(2),
        },
        cpuCount: os.cpus().length,
        platform: os.platform(),
      },
      timestamp: new Date(),
    };

    /* ---------------------------
       Store in Redis
    ---------------------------- */
    if (redisClient?.isOpen) {
      await redisClient.set(
        CACHE_KEY,
        JSON.stringify(stats),
        { EX: CACHE_TTL }
      );
    }

    return res.status(200).json({
      success: true,
      cached: false,
      data: stats,
    });

  } catch (error) {
    console.error("System stats error:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch system stats",
    });
  }
};
