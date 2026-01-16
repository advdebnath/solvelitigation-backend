import { Request, Response } from "express";
import cfg from "@/config";

const logout = (req: Request, res: Response) => {
  res.clearCookie(cfg.AUTH_COOKIE_NAME);
  return res.json({ success: true, message: "Logged out" });
};

export default logout;
