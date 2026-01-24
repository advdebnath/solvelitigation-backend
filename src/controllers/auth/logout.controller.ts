import { Request, Response } from "express";
import cfg from "@/config";

export const logout = (_req: Request, res: Response) => {
  res.clearCookie(cfg.AUTH_COOKIE_NAME);
  return res.json({ success: true, message: "Logged out" });
};
