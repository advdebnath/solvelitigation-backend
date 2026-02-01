import { Request, Response, NextFunction } from "express";
import { PLAN_CAPABILITIES, PlanKey } from "@/config/planCapabilities";

/**
 * Enforce feature availability based on plan
 * Usage: requirePlanFeature("aiTools")
 */
export function requirePlanFeature(
  feature: keyof (typeof PLAN_CAPABILITIES)[PlanKey]["features"]
) {
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

    const allowed = planConfig.features[feature];

    if (!allowed) {
      return res.status(403).json({
        success: false,
        message: `Your plan does not allow access to ${feature}`,
        upgradeRequired: true,
        requiredPlan: "premium",
      });
    }

    next();
  };
}
