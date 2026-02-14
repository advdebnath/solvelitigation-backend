import { Request, Response } from "express";
import bcrypt from "bcryptjs";

import { setAuthCookie } from "../../utils/authCookie";
import { signToken } from "../../utils/jwt";
import { User } from "../../models/user.model";

/**
 * POST /api/auth/login
 */
export const login = async (req: Request, res: Response) => {
  try {
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

    const user = await User.findOne({ email: normalizedEmail }).select(
      "+password"
    );

    if (!user) {
      return res.status(401).json({
        success: false,
        message: "Invalid credentials",
      });
    }

    const isMatch = await bcrypt.compare(password, user.password);

    if (!isMatch) {
      return res.status(401).json({
        success: false,
        message: "Invalid credentials",
      });
    }

    // ✅ Generate JWT
    const token = signToken({
      userId: user._id.toString(),
      role: user.role,
    });

    // ✅ Set auth cookie
    setAuthCookie(res, token);

    return res.status(200).json({
      success: true,
      token,
      user: {
        id: user._id,
        email: user.email,
        role: user.role,
      },
    });
  } catch (error) {
    console.error("LOGIN ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Login failed",
    });
  }
};
