import { Request, Response } from "express";
import mongoose from "mongoose";
import User from "../../models/user.model";

export async function me(req: Request, res: Response) {
  try {
    const jwtUser = (req as any).user || (req as any).currentUser;

    if (!jwtUser?.userId) {
      return res.status(401).json({ message: "Not authenticated" });
    }

    // 🔑 CRITICAL FIX
    const userId = new mongoose.Types.ObjectId(jwtUser.userId);

    const user = await User.findOne({ _id: userId }).select("-password");

    if (!user) {
      return res.status(401).json({ message: "User not found" });
    }

    return res.json({
      success: true,
      user,
    });
  } catch (error) {
    console.error("ME ERROR:", error);
    return res.status(500).json({ message: "Server error" });
  }
}
