"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.getMe = getMe;
const user_model_1 = require("../../models/user.model");
const planLimits_1 = require("../../config/planLimits");
/**
 * GET /api/auth/me
 * Authoritative user session endpoint
 */
async function getMe(req, res) {
    const authUser = req.currentUser;
    if (!authUser) {
        return res.status(401).json({
            success: false,
            message: "Unauthorized",
        });
    }
    // ✅ Strongly typed DB fetch
    const user = (await user_model_1.User.findById(authUser._id)
        .select("name email role plan planStatus planExpiresAt usage grace isVerified")
        .lean());
    if (!user) {
        return res.status(401).json({
            success: false,
            message: "User not found",
        });
    }
    const plan = user.plan;
    const limits = planLimits_1.PLAN_LIMITS[plan];
    return res.json({
        success: true,
        user: {
            id: user._id.toString(),
            name: user.name,
            email: user.email,
            role: user.role,
            plan: user.plan,
            planStatus: user.planStatus,
            planExpiresAt: user.planExpiresAt ?? null,
            isVerified: user.isVerified,
            usage: {
                downloads: user.usage?.downloads ?? 0,
                aiRequests: user.usage?.aiRequests ?? 0,
                judgmentsViewed: user.usage?.judgmentsViewed ?? 0,
            },
            grace: user.grace ?? null,
            limits,
        },
    });
}
