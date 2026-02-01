// src/config.ts

export const COOKIE_OPTIONS = {
  httpOnly: true,
  secure: process.env.NODE_ENV === "production",
  sameSite: "lax" as const,
};

export const JWT_COOKIE_NAME = "sl_auth";
