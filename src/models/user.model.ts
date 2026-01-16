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

    password: {
      type: String,
      required: true,
      select: false, // 🔒 never exposed
    },

    phone: {
      type: String,
      trim: true,
      sparse: true,
    },

    state: {
      type: String,
      trim: true,
    },

    district: {
      type: String,
      trim: true,
    },

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
required: true,
    },

    planStatus: {
      type: String,
      enum: ["active", "inactive", "expired"],
      default: "active",
    },

    planExpiresAt: {
      type: Date,
      default: null,
    },

    usage: {
      downloads: { type: Number, default: 0 },
      aiRequests: { type: Number, default: 0 },
      judgmentsViewed: { type: Number, default: 0 },
    },

    grace: {
      downloads: { type: Number, default: 0 },
      aiRequests: { type: Number, default: 0 },
      judgmentsViewed: { type: Number, default: 0 },
    },

usageMeta: {
  judgmentsViewedAt: {
    type: Date,
    default: null,
  },
},





    /**
     * EMAIL VERIFICATION
     */
    isVerified: {
      type: Boolean,
      default: false,
      index: true,
    },

    /**
     * SOFT DELETE
     */
    isDeleted: {
      type: Boolean,
      default: false,
    },

    deletedAt: {
      type: Date,
      default: null,
    },

    /**
     * AUTO-EXPIRE UNVERIFIED USERS (TTL)
     * MongoDB will delete the document automatically
     */
    verificationExpiresAt: {
      type: Date,
      default: () =>
        new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
      index: { expires: 0 },
    },
  },
  {
    timestamps: true,
    versionKey: false,
  }
);

/**
 * =========================
 * MODEL EXPORT
 * =========================
 */
export const User =
  mongoose.models.User || mongoose.model<IUser>("User", UserSchema);
