import { Request, Response, NextFunction } from "express";
import { User, IUser } from "@/models/user.model";

/**
 * Guards feature usage based on plan
 * DOES NOT increment usage
 * DOES NOT modify controllers
 */
export const planGuard =
  (feature: "download" | "ai" | "view") =>
  async (req: Request, res: Response, next: NextFunction) => {
    try {
      const userId = res.locals.userId;

      if (!userId) {
        return res.status(401).json({
          success: false,
          message: "Unauthenticated",
        });
      }

      const user = await User.findById(userId).lean<IUser>();

      if (!user) {
        return res.status(401).json({
          success: false,
          message: "User not found",
        });
      }

      const plan = user.plan || "free";
      const usage = user.usage || {};
      const grace = user.grace || {};

      const LIMITS: Record<
        string,
        { download: number; ai: number; view: number }
      > = {
        free: { download: 0, ai: 0, view: 5 },
        simple: { download: 50, ai: 20, view: 200 },
        premium: {
          download: Number.POSITIVE_INFINITY,
          ai: Number.POSITIVE_INFINITY,
          view: Number.POSITIVE_INFINITY,
        },
        enterprise: {
          download: Number.POSITIVE_INFINITY,
          ai: Number.POSITIVE_INFINITY,
          view: Number.POSITIVE_INFINITY,
        },
      };

      const used =
        feature === "download"
          ? usage.downloads ?? 0
          : feature === "ai"
          ? usage.aiRequests ?? 0
          : usage.judgmentsViewed ?? 0;

      const limit = LIMITS[plan]?.[feature] ?? 0;

      // Allowed within plan
      if (used < limit) {
        return next();
      }

      // Grace allowance (5 max)
      const graceUsed =
        feature === "download"
          ? grace.downloads ?? 0
          : feature === "ai"
          ? grace.aiRequests ?? 0
          : grace.judgmentsViewed ?? 0;

      if (graceUsed < 5) {
        return next();
      }

      // Block
      return res.status(403).json({
        success: false,
        code: "PLAN_LIMIT_REACHED",
        message: "Plan limit reached. Please upgrade.",
      });
    } catch (err) {
      console.error("[PLAN GUARD ERROR]", err);
      return res.status(500).json({
        success: false,
        message: "Plan enforcement failed",
      });
    }
  };
