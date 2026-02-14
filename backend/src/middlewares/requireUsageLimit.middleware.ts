import { Request, Response, NextFunction } from "express";
import { PLAN_LIMITS } from "@/config/planLimits";
import { UsageKey, PlanType } from "@/types/plan.types";

export const requireUsageLimit =
  (key: UsageKey) =>
  (req: Request, res: Response, next: NextFunction) => {
    const user = req.user || req.currentUser;

    if (!user || !user.plan) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    // 🔒 HARD NARROWING — this is what TS needs
    const plan = user.plan as PlanType;
    const limits = PLAN_LIMITS[plan];

    const used = typeof (user.usage?.[key as keyof typeof user.usage]) === "number"
      ? (user.usage?.[key as keyof typeof user.usage] as number)
      : 0;
      user.usage && key in user.usage
        ? user.usage[key as keyof typeof user.usage] ?? 0
        : 0;

    const grace =
      user.grace && key in user.grace
        ? user.grace[key as keyof typeof user.grace] ?? 0
        : 0;

    if (used >= limits[key] && grace <= 0) {
      return res.status(429).json({
        message: "Usage limit exceeded for your plan",
      });
    }

    next();
  };
