import { Router, Request, Response } from "express";
import mongoose from "mongoose";

import User from "../models/user.model";

import auth from "../middleware/auth.middleware";
import { requireRole } from "../middleware/requireRole";

import {
  getIngestionStats,
  getFailedIngestions,
  retryFailedIngestion,
} from "../controllers/admin/ingestion.monitor.controller";

import { getSystemHealth } from "../controllers/admin/systemHealth.controller";
import { getSystemResources } from "../controllers/admin/systemResources.controller";
import { getSystemStats } from "../controllers/admin/systemStats.controller";

const router = Router();

/* =====================================================
   🔐 SUPERADMIN PROTECTED ROUTES
===================================================== */

/**
 * 🔥 MAIN DASHBOARD STATS (FIX FOR FRONTEND)
 * → This is what your UI is calling: /api/admin/stats
 */
router.get(
  "/stats",
  auth,
  requireRole(["superadmin"]),
  async (_req: Request, res: Response) => {
    try {
      const db = mongoose.connection.db;

      if (!db) {
        return res.status(500).json({
          success: false,
          message: "DB not connected",
        });
      }

      const totalUsers = await db.collection(
        "users"
      ).countDocuments();

      const totalJudgments = await db.collection(
        "judgments"
      ).countDocuments();

      const totalIngestions = await db.collection(
        "judgmentingestions"
      ).countDocuments({
        status: "COMPLETED"
      });

      const categories = await db.collection("judgments")
        .aggregate([
          { $group: { _id: "$category", count: { $sum: 1 } } }
        ])
        .toArray();

      res.json({
        success: true,
        data: {
          totalUsers,
          totalJudgments,
          totalIngestions,
          categories,
        },
      });

    } catch (err) {
      console.error("❌ Admin Stats Error:", err);
      res.status(500).json({
        success: false,
        message: "Stats fetch failed",
      });
    }
  }
);

/**
 * 📊 Full system stats (production metrics)
 */

/**
 * 👥 USERS MANAGEMENT
 */
router.get(
  "/users",
  auth,
  requireRole(["superadmin"]),
  async (req: Request, res: Response) => {

    try {

      const page = Number(req.query.page || 1);

      const limit = 10;

      const search = String(
        req.query.search || ""
      );

      const skip = (page - 1) * limit;

      // =============================================
      // 🔥 SEARCH FILTER
      // =============================================

      const filter = search
        ? {
            $or: [

              {
                name: {
                  $regex: search,
                  $options: "i"
                }
              },

              {
                email: {
                  $regex: search,
                  $options: "i"
                }
              }
            ]
          }
        : {};

      // =============================================
      // 🔥 FETCH USERS
      // =============================================

      const users = await User.find(filter)

        .select(
          "name email role createdAt"
        )

        .sort({
          createdAt: -1
        })

        .skip(skip)

        .limit(limit)

        .lean();

      const totalUsers =
        await User.countDocuments(filter);

      const totalPages = Math.ceil(
        totalUsers / limit
      );

      return res.json({

        success: true,

        users,

        page,

        totalPages,

        totalUsers
      });

    } catch (err) {

      console.error(
        "❌ Users Fetch Error:",
        err
      );

      return res.status(500).json({

        success: false,

        message: "Failed to fetch users"
      });
    }
  }
);



router.get(
  "/system-stats",
  auth,
  requireRole(["superadmin"]),
  getSystemStats
);

/**
 * 📦 Ingestion stats breakdown
 */
router.get(
  "/ingestion-stats",
  auth,
  requireRole(["superadmin"]),
  getIngestionStats
);

/**
 * ❤️ System health check (DB + Redis)
 */
router.get(
  "/system-health",
  auth,
  requireRole(["superadmin"]),
  getSystemHealth
);

/**
 * 🖥 System resource usage (CPU / Memory)
 */
router.get(
  "/system-resources",
  auth,
  requireRole(["superadmin"]),
  getSystemResources
);

/**
 * 🔁 Retry ALL failed ingestions (FIXED)
 */
router.post(
  "/retry-failed",
  auth,
  requireRole(["superadmin"]),
  async (_req: Request, res: Response) => {
    try {
      const db = mongoose.connection.db;

      if (!db) {
        return res.status(500).json({ success: false });
      }

      const failed = await db.collection("judgmentingestions").find({
        status: "FAILED"
      }).toArray();

      const ids = failed.map(f => f._id);

      await db.collection("judgmentingestions").updateMany(
        { _id: { $in: ids } },
        {
          $set: {
            status: "QUEUED",
            retryCount: 0,
            error: null
          }
        }
      );

      res.json({
        success: true,
        retried: ids.length
      });

    } catch (err) {
      console.error("❌ Retry all failed error:", err);
      res.status(500).json({ success: false });
    }
  }
);

/* =====================================================
   🔥 INGESTION MANAGEMENT
===================================================== */

/**
 * ❌ Failed ingestion list
 */
router.get(
  "/ingestions/failed",
  auth,
  requireRole(["superadmin"]),
  getFailedIngestions
);

/**
 * 🔁 Retry single ingestion
 */
router.post(
  "/ingestions/retry/:id",
  auth,
  requireRole(["superadmin"]),
  retryFailedIngestion
);

/**
 * 📊 Ingestion stats (duplicate safe route)
 */
router.get(
  "/ingestions/stats",
  auth,
  requireRole(["superadmin"]),
  getIngestionStats
);

export default router;
