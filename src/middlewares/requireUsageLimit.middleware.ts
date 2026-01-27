import { Request, Response, NextFunction } from "express";
import { PLAN_CAPABILITIES, PlanKey } from "@/config/planCapabilities";

/**
 * Enforce per-day usage limits based on plan
 *
 * Usage:
 *   requireUsageLimit("judgments")
 *   requireUsageLimit("downloads")
 *   requireUsageLimit("aiRequests")
 */
type UsageKey = "judgments" | "downloads" | "aiRequests";

export function requireUsageLimit(key: UsageKey) {
  return (req: Request, res: Response, next: NextFunction) => {
    const user = req.user || req.currentUser;

    if (!user) {
      return res.status(401).json({
        success: false,
        message: "Authentication required",
      });
    }

    // 🔓 Superadmin bypass
    if (user.role === "superadmin") {
      return next();
    }

    const plan = (user.plan || "free") as PlanKey;
    const planConfig = PLAN_CAPABILITIES[plan];

    if (!planConfig) {
      return res.status(403).json({
        success: false,
        message: "Invalid subscription plan",
      });
    }

    // 🔁 Map usage key → plan capability
    const planLimitMap = {
      judgments: planConfig.judgmentsPerDay,
      downloads: planConfig.downloadsPerDay,
      aiRequests: planConfig.aiRequestsPerDay,
    } as const;

    const limit = planLimitMap[key];

    // Unlimited plan
    if (limit === "unlimited") {
      return next();
    }

    const used = user.usage?.[key] ?? 0;
    const grace = user.grace?.[key] ?? 0;

    if (used >= limit + grace) {
      return res.status(429).json({
        success: false,
        message: `Daily ${key} limit reached`,
        limit,
        used,
        upgradeRequired: true,
        requiredPlan: "premium",
      });
    }

    next();
  };
}
