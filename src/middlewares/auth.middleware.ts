import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import mongoose from "mongoose";

import { User } from "@/models/user.model";
import { IUser } from "@/models/user.types";
import config from "@/config";
import { PlanType } from "@/types/plan.types";

/**
 * Core auth middleware
 */
export async function authenticateJWT(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token =
      req.cookies?.[config.AUTH_COOKIE_NAME] ||
      req.headers.authorization?.replace("Bearer ", "");

    if (!token) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    const decoded = jwt.verify(token, config.jwtSecret) as {
      userId: string;
    };

    if (!mongoose.Types.ObjectId.isValid(decoded.userId)) {
      return res.status(401).json({ message: "Invalid token" });
    }

    const user = (await User.findOne({
      _id: decoded.userId,
      isDeleted: false,
    }).lean()) as IUser | null;

    if (!user) {
      return res.status(401).json({ message: "User not found" });
    }

    const normalizedUser = {
      _id: user._id.toString(),
      name: user.name,
      email: user.email,
      role: user.role,

      plan: user.plan as PlanType,
      planStatus: user.planStatus,
      planExpiresAt: user.planExpiresAt ?? null,

      usage: user.usage ?? {
        downloads: 0,
        aiRequests: 0,
        judgmentsViewed: 0,
      },

      grace: user.grace ?? null,
      isVerified: user.isVerified,
    };

    // ✅ Backward compatibility
    req.user = normalizedUser;
    req.currentUser = normalizedUser;

    next();
  } catch {
    return res.status(401).json({ message: "Authentication failed" });
  }
}

/**
 * Superadmin guard
 */
export function requireSuperAdmin(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const user = req.user || req.currentUser;

  if (!user || user.role !== "superadmin") {
    return res.status(403).json({
      success: false,
      message: "Superadmin access required",
    });
  }

  next();
}
