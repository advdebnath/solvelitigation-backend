"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.User = void 0;
const mongoose_1 = __importStar(require("mongoose"));
/**
 * =========================
 * USER SCHEMA
 * =========================
 */
const UserSchema = new mongoose_1.Schema({
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
        default: () => new Date(Date.now() + 7 * 24 * 60 * 60 * 1000), // 7 days
        index: { expires: 0 },
    },
}, {
    timestamps: true,
    versionKey: false,
});
/**
 * =========================
 * MODEL EXPORT
 * =========================
 */
exports.User = mongoose_1.default.models.User || mongoose_1.default.model("User", UserSchema);
