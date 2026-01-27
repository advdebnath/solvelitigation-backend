import { Request, Response, NextFunction } from "express";
import { PLAN_LIMITS } from "@/config/planLimits";
import { PlanType, UsageKey } from "@/types/plan.types";
import { User } from "../models/user.model";

/**
 * Enforce plan usage limits with grace support
 */
export const enforcePlanLimit =
  (key: UsageKey) =>
  async (req: Request, res: Response, next: NextFunction) => {
    if (!req.currentUser) {
      return res.status(401).json({ success: false });
    }

    const user = await User.findById(req.currentUser._id).select(
      "plan usage grace planStatus"
    );

    if (!user) {
      return res.status(401).json({ success: false });
    }

    const plan = user.plan as PlanType;
    const limits = PLAN_LIMITS[plan];

    // Unlimited plans (enterprise)
    if (limits[key] === Infinity) {
      return next();
    }

    const used = user.usage[key];
    const allowed = limits[key];

    // Within plan limit
    if (used < allowed) {
      return next();
    }

    // Use grace if available
    if (user.grace[key] > 0) {
      user.grace[key] -= 1;
      await user.save();
      return next();
    }

    // Hard block
    return res.status(402).json({
      success: false,
      message: "Plan limit exceeded",
      code: "PLAN_LIMIT_REACHED",
    });
  };
