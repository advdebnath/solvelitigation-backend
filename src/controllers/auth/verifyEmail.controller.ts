import { Request, Response } from "express";
import { User } from "@/models/user.model";

/**
 * GET /api/auth/verify-email?token=XXXX
 * Verifies user email using token
 */
export const verifyEmail = async (req: Request, res: Response) => {
  try {
    const { token } = req.query;

    if (!token || typeof token !== "string") {
      return res.status(400).json({
        success: false,
        message: "Invalid or missing verification token",
      });
    }

    const user = await User.findOne({
      verificationToken: token,
      verificationTokenExpires: { $gt: new Date() },
    });

    if (!user) {
      return res.status(400).json({
        success: false,
        message: "Verification token expired or invalid",
      });
    }

    // ✅ Verify user
    user.isVerified = true;
    user.verificationToken = undefined;
    user.verificationTokenExpires = undefined;

    await user.save();

    return res.json({
      success: true,
      message: "Email verified successfully. You may now log in.",
    });
  } catch (error) {
    console.error("[VERIFY EMAIL ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Email verification failed",
    });
  }
};
