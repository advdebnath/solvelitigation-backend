// src/middlewares/auth.middleware.ts

import { Request, Response, NextFunction } from "express";
import jwt from "jsonwebtoken";
import mongoose from "mongoose";

import UserModel from "../models/user.model";
import { IUser } from "../models/user.types";
import { JWT_COOKIE_NAME } from "../config";
import { PlanType } from "../types/plan.types";

/**
 * ===============================
 * AUTHENTICATE JWT (CORE)
 * ===============================
 */
export async function authenticateJWT(
  req: Request,
  res: Response,
  next: NextFunction
) {
  try {
    const token =
      req.cookies?.[JWT_COOKIE_NAME] ||
      req.headers.authorization?.replace("Bearer ", "");

    if (!token) {
      return res.status(401).json({ message: "Unauthorized" });
    }

    // 🔐 Verify token
    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET as string
    ) as { userId: string; role?: string };

    if (!decoded.userId || !mongoose.Types.ObjectId.isValid(decoded.userId)) {
      return res.status(401).json({ message: "Invalid token" });
    }

    // 👤 Fetch user
    const user = (await UserModel.findOne({
      _id: decoded.userId,
      isDeleted: { $ne: true },
    }).lean()) as IUser | null;

    if (!user) {
      return res.status(401).json({ message: "User not found" });
    }

    // 🧠 Normalize user object
    const normalizedUser = {
      _id: user._id.toString(),
      userId: user._id.toString(), // for /me
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
      isVerified: user.isVerified ?? false,
    };

    // 🔁 Backward compatibility
    (req as any).user = normalizedUser;
    (req as any).currentUser = normalizedUser;

    next();
  } catch (error) {
    return res.status(401).json({ message: "Authentication failed" });
  }
}

/**
 * ===============================
 * SUPERADMIN GUARD
 * ===============================
 */
export function requireSuperAdmin(
  req: Request,
  res: Response,
  next: NextFunction
) {
  const user = (req as any).user || (req as any).currentUser;

  if (!user || user.role !== "superadmin") {
    return res.status(403).json({
      success: false,
      message: "Superadmin access required",
    });
  }

  next();
}

/**
 * ===============================
 * ALIAS (IMPORTANT)
 * ===============================
 * This fixes:
 *   import { auth } from "../middlewares/auth.middleware"
 */
export const auth = authenticateJWT;
