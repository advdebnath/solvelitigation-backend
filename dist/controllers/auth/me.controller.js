"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.default = getMe;
const user_model_1 = __importDefault(require("../../models/user.model"));
async function getMe(req, res) {
    try {
        if (!req.user?.userId) {
            return res.status(401).json({
                success: false,
                message: "Not authenticated",
            });
        }
        const user = (await user_model_1.default.findById(req.user.userId)
            .select("_id name email role")
            .lean());
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
    }
    catch (err) {
        return res.status(500).json({
            success: false,
            message: "Failed to fetch user",
        });
    }
}
