import { Request, Response } from "express";
import bcrypt from "bcryptjs";
import { User } from "@/models/user.model";

/**
 * POST /api/auth/register
 */
export const register = async (req: Request, res: Response) => {
  try {
    const {
      name,
      email,
      password,
      phone,
      state,
      district,
      plan,
    } = req.body;

    // 🔐 Required fields
    if (!name || !email || !password) {
      return res.status(400).json({
        success: false,
        message: "Name, email and password are required",
      });
    }

    // 📧 Check existing email
    const existing = await User.findOne({ email });
    if (existing) {
      return res.status(400).json({
        success: false,
        message: "Email already registered",
      });
    }

    // 📦 Validate plan if provided
    const allowedPlans = ["free", "simple", "premium", "enterprise"];
    if (plan && !allowedPlans.includes(plan)) {
      return res.status(400).json({
        success: false,
        message: "Invalid plan selected",
      });
    }

    // 🔑 Hash password
    const hashedPassword = await bcrypt.hash(password, 10);

    // 👤 Create user
    const user = await User.create({
      name,
      email,
      password: hashedPassword,

      // optional (future-ready)
      phone,
      state,
      district,

      plan: plan || "free",
      planStatus: "active",
      role: "user",
    });

    return res.status(201).json({
      success: true,
      message: "Registration successful. Please verify your email.",
      userId: user._id,
    });
  } catch (err: any) {
    console.error("REGISTER ERROR:", err);
    return res.status(500).json({
      success: false,
      message: "Registration failed",
    });
  }
};
