import mongoose, { Schema, Document } from "mongoose";

/**
 * =========================
 * USER INTERFACE
 * =========================
 */
export interface IUser extends Document {
  name: string;
  email: string;
  password: string;

  phone?: string;
  state?: string;
  district?: string;

  role: "user" | "admin" | "superadmin";

  plan: "free" | "simple" | "premium" | "enterprise";
  planStatus: "active" | "inactive" | "expired";
  planExpiresAt?: Date | null;

  usage: {
    downloads: number;
    aiRequests: number;
    judgmentsViewed: number;
    lastViewedAt?: Date;
  };

  grace: {
    downloads: number;
    aiRequests: number;
    judgmentsViewed: number;
  };

  isVerified: boolean;

  /** Soft delete */
  isDeleted: boolean;
  deletedAt?: Date | null;

  /** Email verification expiry (TTL) */
  verificationExpiresAt?: Date | null;

  createdAt: Date;
  updatedAt: Date;
}

/**
 * =========================
 * USER SCHEMA
 * =========================
 */
const UserSchema = new Schema<IUser>(
  {
    name: {
      type: String,
      required: true,
      trim: true,
    },

    email: {
      type: String,
      required: true,
      unique: true,
      lowercase: true,
      trim: true,
      index: true,
    },

    /** 🔥 CRITICAL FIX */
    password: {
      type: String,
      required: true,
      select: false, // 👈 THIS FIXES LOGIN
    },

    phone: String,
    state: String,
    district: String,

    role: {
      type: String,
      enum: ["user", "admin", "superadmin"],
      default: "user",
      index: true,
    },

    plan: {
      type: String,
      enum: ["free", "simple", "premium", "enterprise"],
      default: "free",
    },

    planStatus: {
      type: String,
      enum: ["active", "inactive", "expired"],
      default: "inactive",
    },

    planExpiresAt: {
      type: Date,
      default: null,
    },

    /** ✅ FIXED: schema now matches interface */
    usage: {
      downloads: { type: Number, default: 0 },
      aiRequests: { type: Number, default: 0 },
      judgmentsViewed: { type: Number, default: 0 },
      lastViewedAt: { type: Date },
    },

    grace: {
      downloads: { type: Number, default: 0 },
      aiRequests: { type: Number, default: 0 },
      judgmentsViewed: { type: Number, default: 0 },
    },

    isVerified: {
      type: Boolean,
      default: false,
    },

    isDeleted: {
      type: Boolean,
      default: false,
      index: true,
    },

    deletedAt: {
      type: Date,
      default: null,
    },

    verificationExpiresAt: {
      type: Date,
      default: null,
      index: { expireAfterSeconds: 0 },
    },
  },
  {
    timestamps: true,
  }
);

export const User = mongoose.model<IUser>("User", UserSchema);
export default User;

