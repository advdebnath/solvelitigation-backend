import rateLimit from "express-rate-limit";

/**
 * General API limiter
 * Protects all API routes
 */
export const apiLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 1000, // 1000 requests per IP per 15 minutes
  standardHeaders: true,
  legacyHeaders: false,
});

/**
 * Strict limiter for login endpoint
 * Protects against brute-force attacks
 */
export const authLimiter = rateLimit({
  windowMs: 15 * 60 * 1000, // 15 minutes
  max: 10, // only 10 login attempts per IP
  standardHeaders: true,
  legacyHeaders: false,
});
