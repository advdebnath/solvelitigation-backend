import { Request, Response } from "express";
import User from "../../models/user.model";

interface SafeUser {
  _id: string;
  name: string;
  email: string;
  role: string;
}

export default async function getMe(req: Request, res: Response) {
  try {
    if (!req.user?.userId) {
      return res.status(401).json({
        success: false,
        message: "Not authenticated",
      });
    }

    const user = (await User.findById(req.user.userId)
      .select("_id name email role")
      .lean()) as SafeUser | null;

    if (!user) {
      return res.status(404).json({
        success: false,
        message: "User not found",
      });
    }

    return res.json({
      success: true,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
      },
    });
  } catch (err) {
    return res.status(500).json({
      success: false,
      message: "Failed to fetch user",
    });
  }
}
