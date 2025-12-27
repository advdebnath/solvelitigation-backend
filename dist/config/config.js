"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const config = {
    jwtSecret: process.env.JWT_SECRET || "dev-secret",
    env: process.env.NODE_ENV || "development",
    AUTH_COOKIE_NAME: process.env.AUTH_COOKIE_NAME || "sl_auth",
};
exports.default = config;
