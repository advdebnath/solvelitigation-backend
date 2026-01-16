"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const config_1 = __importDefault(require("../../config"));
const logout = (req, res) => {
    res.clearCookie(config_1.default.AUTH_COOKIE_NAME);
    return res.json({ success: true, message: "Logged out" });
};
exports.default = logout;
