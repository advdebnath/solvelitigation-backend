import { Request, Response, NextFunction } from "express";
import { PlanType } from "@/types/plan.types";

/**
 * Require specific plans
 */
export const requirePlan =
  (...plans: PlanType[]) =>
  (req: Request, res: Response, next: NextFunction) => {
    const user = req.user || req.currentUser;

    if (!user || !plans.includes(user.plan)) {
      return res.status(403).json({
        success: false,
        message: "Your subscription plan does not allow this action",
      });
    }

    next();
  };

/**
 * Require active plan
 */
export const requireActivePlan = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const user = req.user || req.currentUser;

  if (!user || user.planStatus !== "active") {
    return res.status(403).json({
      success: false,
      message: "Your subscription is inactive or expired",
    });
  }

  next();
};
