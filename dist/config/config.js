"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
const config = {
    jwtSecret: process.env.JWT_SECRET || 'dev-secret',
    env: process.env.NODE_ENV || 'development',
};
exports.default = config;
