import { Request, Response } from "express";
import mongoose from "mongoose";
import bcrypt from "bcryptjs";
import { User } from "@/models/user.model";
import { signToken } from "@/utils/jwt";
import { setAuthCookie } from "@/utils/authCookie";

/**
 * POST /api/auth/login
 * Secure login with httpOnly JWT cookie
 */
export const login = async (req: Request, res: Response) => {
  try {
    // 1️⃣ Ensure DB is ready
    if (mongoose.connection.readyState !== 1) {
      return res.status(503).json({
        success: false,
        message: "Database not ready",
      });
    }

    // 2️⃣ Validate input
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

    // 3️⃣ Normalize email
    const normalizedEmail = email.toLowerCase().trim();

    // 4️⃣ Fetch user
    const user = await User.findOne({ email: normalizedEmail }).select(
      "+password"
    );
if (!user) {
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

if (user.isDeleted) {
  return res.status(403).json({
    success: false,
    message: "Account has been deactivated",
  });
}



    // 5️⃣ Prevent timing attacks
    if (!user) {
      await bcrypt.compare(
        password,
        "$2a$10$invalidinvalidinvalidinvalidinvalidinvalid"
      );
      return res.status(401).json({
        success: false,
        message: "Invalid credentials",
      });
    }

    // 6️⃣ Verify password
    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: "Invalid email or password",
      });
    }



// ❌ Block unverified users
if (!user.isVerified) {
  return res.status(403).json({
    success: false,
    message: "Please verify your email before logging in",
  });
}



    // 7️⃣ Ensure email is verified
    if (!user.isVerified) {
      return res.status(403).json({
        success: false,
        code: "EMAIL_NOT_VERIFIED",
        message: "Please verify your email before logging in",
      });
    }

    // 8️⃣ Generate JWT
    const token = signToken({
      userId: user._id.toString(),
      role: user.role,
    });

    // 9️⃣ Set secure httpOnly cookie
    setAuthCookie(res, token);

    // 🔟 Respond with safe user payload (NO token)
    return res.status(200).json({
      success: true,
      user: {
        id: user._id,
        name: user.name,
        email: user.email,
        role: user.role,
      },
    });
  } catch (error) {
    console.error("[LOGIN ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Login failed",
    });
  }
};
