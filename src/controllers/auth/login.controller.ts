import { Request, Response } from "express";
import mongoose from "mongoose";
import bcrypt from "bcryptjs";
import { User } from "@/models/user.model";
import { signToken } from "@/utils/jwt";
import { setAuthCookie } from "@/utils/authCookie";

export const login = async (req: Request, res: Response) => {
  try {
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({
        success: false,
        message: "Database not ready",
      });
    }

    const { email, password } = req.body as {
      email?: string;
      password?: string;
    };

    if (!email || !password) {
      return res.status(400).json({
        success: false,
        message: "Email and password required",
      });
    }

    const normalizedEmail = email.toLowerCase().trim();


const user = await User.findOne({ email: normalizedEmail }).select("+password");

if (!user || user.isDeleted) {
  return res.status(401).json({
    success: false,
    message: "Invalid email or password",
  });
}

if (!user.isVerified) {
  return res.status(403).json({
    success: false,
    code: "EMAIL_NOT_VERIFIED",
    message: "Please verify your email before logging in",
  });
}

const isMatch = await bcrypt.compare(password, user.password);

if (!isMatch) {
  return res.status(401).json({
    success: false,
    message: "Invalid email or password",
  });
}

    const token = signToken({
      userId: user._id.toString(),
      role: user.role,
    });

    setAuthCookie(res, token);

    return res.status(200).json({
      success: true,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
        plan: user.plan,
      },
    });
  } catch (err) {
    console.error("[LOGIN ERROR]", err);
    return res.status(500).json({
      success: false,
      message: "Login failed",
    });
  }
};
