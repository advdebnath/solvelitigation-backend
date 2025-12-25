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
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.requireSuperAdmin = exports.requireAdmin = exports.authorizeRoles = exports.requireRole = exports.authenticateJWTOptional = exports.optionalAuth = exports.authenticateJWT = void 0;
exports.requireAdminOrSuperAdmin = requireAdminOrSuperAdmin;
const config_1 = __importDefault(require("../config"));
const jwt = __importStar(require("jsonwebtoken"));
const jwt_1 = require("../utils/jwt");
const COOKIE_NAME = process.env.AUTH_COOKIE_NAME || "sl_auth";
const JWT_SECRET = config_1.default.jwtSecret ||
    config_1.default?.jwtSecret ||
    process.env.JWT_SECRET ||
    "supersecret";
/* -------------------------------------------------------------------------- */
/* 🔒 Primary Authentication Middleware (Bearer preferred, Cookie fallback)   */
/* -------------------------------------------------------------------------- */
const authenticateJWT = (req, res, next) => {
    try {
        let token;
        const authHeader = req.headers.authorization;
        if (authHeader?.startsWith("Bearer "))
            token = authHeader.split(" ")[1];
        if (!token && req.cookies?.[COOKIE_NAME])
            token = req.cookies[COOKIE_NAME];
        if (!token) {
            return res.status(401).json({ success: false, message: "Unauthorized" });
        }
        let payload;
        try {
            payload = (0, jwt_1.verifyToken)(token, JWT_SECRET);
        }
        catch {
            payload = jwt.verify(token, JWT_SECRET);
        }
        const userId = payload.sub || payload._id || payload.id;
        if (!userId) {
            return res
                .status(401)
                .json({ success: false, message: "Invalid token payload" });
        }
        req.user = {
            id: String(userId),
            email: payload.email ?? "",
            role: payload.role ?? "user",
        };
        req.auth = payload;
        next();
    }
    catch (err) {
        console.error("[auth.middleware] Invalid JWT:", err);
        return res
            .status(401)
            .json({ success: false, message: "Invalid or expired token" });
    }
};
exports.authenticateJWT = authenticateJWT;
const optionalAuth = (req, _res, next) => {
    let token;
    const authHeader = req.headers.authorization;
    if (authHeader?.startsWith("Bearer "))
        token = authHeader.split(" ")[1];
    if (!token && req.cookies?.[COOKIE_NAME])
        token = req.cookies[COOKIE_NAME];
    if (token) {
        try {
            let payload;
            try {
                payload = (0, jwt_1.verifyToken)(token, JWT_SECRET);
            }
            catch {
                payload = jwt.verify(token, JWT_SECRET);
            }
            const userId = payload.sub || payload._id || payload.id;
            if (userId) {
                req.user = {
                    id: String(userId),
                    email: payload.email ?? "",
                    role: payload.role ?? "user",
                };
                req.auth = payload;
            }
        }
        catch {
            console.warn("[auth.middleware] Optional auth ignored");
        }
    }
    next();
};
exports.optionalAuth = optionalAuth;
exports.authenticateJWTOptional = exports.optionalAuth;
/* -------------------------------------------------------------------------- */
/* 🔐 Role-Based Access Control                                               */
/* -------------------------------------------------------------------------- */
const requireRole = (role) => {
    return (req, res, next) => {
        if (!req.user || req.user.role !== role) {
            return res.status(403).json({
                success: false,
                message: `Forbidden: ${role} role required`,
            });
        }
        next();
    };
};
exports.requireRole = requireRole;
const authorizeRoles = (...roles) => {
    return (req, res, next) => {
        if (!req.user) {
            return res
                .status(401)
                .json({ success: false, message: "Unauthorized: No user found" });
        }
        if (!roles.includes(req.user.role)) {
            return res.status(403).json({
                success: false,
                message: `Forbidden: requires one of the following roles: ${roles.join(", ")}`,
            });
        }
        next();
    };
};
exports.authorizeRoles = authorizeRoles;
const requireAdmin = (req, res, next) => {
    if (!req.user) {
        return res
            .status(401)
            .json({ success: false, message: "Unauthorized: missing user" });
    }
    if (req.user.role !== "admin" && req.user.role !== "superadmin") {
        return res.status(403).json({
            success: false,
            message: "Forbidden: Only Admins or Superadmin are authorized",
        });
    }
    next();
};
exports.requireAdmin = requireAdmin;
exports.requireSuperAdmin = (0, exports.requireRole)("superadmin");
exports.default = {
    authenticateJWT: exports.authenticateJWT,
    authenticateJWTOptional: exports.authenticateJWTOptional,
    optionalAuth: exports.optionalAuth,
    requireRole: exports.requireRole,
    authorizeRoles: exports.authorizeRoles,
    requireAdmin: exports.requireAdmin,
    requireSuperAdmin: exports.requireSuperAdmin,
};
// ✅ Allow only Admin or Superadmin to proceed
function requireAdminOrSuperAdmin(req, res, next) {
    const user = req.user;
    if (!user) {
        return res
            .status(401)
            .json({ success: false, message: "Not authenticated" });
    }
    if (user.role !== "superadmin" && user.role !== "admin") {
        return res
            .status(403)
            .json({ success: false, message: "Admin or Superadmin required" });
    }
    next();
}
