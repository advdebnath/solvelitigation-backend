import { Request, Response } from "express";
import { User, IUser } from "@/models/user.model";
import { PLAN_LIMITS } from "@/config/planLimits";
import { PlanType } from "@/types/plan.types";

/**
 * GET /api/auth/me
 * Authoritative user session endpoint
 */
export async function getMe(req: Request, res: Response) {
  const authUser = req.currentUser;

  if (!authUser) {
    return res.status(401).json({
      success: false,
      message: "Unauthorized",
    });
  }

  // ✅ Strongly typed DB fetch
  const user = (await User.findById(authUser._id)
    .select(
      "name email role plan planStatus planExpiresAt usage grace isVerified"
    )
    .lean()) as IUser | null;

  if (!user) {
    return res.status(401).json({
      success: false,
      message: "User not found",
    });
  }

  const plan = user.plan as PlanType;
  const limits = PLAN_LIMITS[plan];

  return res.json({
    success: true,
    user: {
      id: user._id.toString(),
      name: user.name,
      email: user.email,
      role: user.role,

      plan: user.plan,
      planStatus: user.planStatus,
      planExpiresAt: user.planExpiresAt ?? null,

      isVerified: user.isVerified,

      usage: {
        downloads: user.usage?.downloads ?? 0,
        aiRequests: user.usage?.aiRequests ?? 0,
        judgmentsViewed: user.usage?.judgmentsViewed ?? 0,
      },

      grace: user.grace ?? null,

      limits,
    },
  });
}
