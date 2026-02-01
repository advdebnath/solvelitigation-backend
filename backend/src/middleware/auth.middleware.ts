import jwt from "jsonwebtoken";
import { Request, Response, NextFunction } from "express";
import { User } from "../models/user.model";

const auth = async (req: Request, res: Response, next: NextFunction) => {
  try {
    const token =
      req.cookies?.sl_auth ||
      req.headers.authorization?.replace("Bearer ", "");

    if (!token) {
      return res.status(401).json({ message: "Not authenticated" });
    }

    const decoded = jwt.verify(
      token,
      process.env.JWT_SECRET as string
    ) as { userId: string };

    const user = await User.findById(decoded.userId).lean();

    if (!user) {
      return res.status(401).json({ message: "User not found" });
    }

    // ✅ MAP to AuthUser (ObjectId → string)
    req.user = {
      _id: user._id.toString(),
      name: user.name,
      email: user.email,
      role: user.role,

      plan: user.plan,
      planStatus: user.planStatus,
      planExpiresAt: user.planExpiresAt ?? null,

      usage: user.usage,
      grace: user.grace,
      isVerified: user.isVerified,
    };

    req.currentUser = req.user;

    next();
  } catch (err) {
    return res.status(401).json({ message: "Invalid token" });
  }
};

export default auth;
