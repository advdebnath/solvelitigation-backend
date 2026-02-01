import { Request, Response } from "express";
import { COOKIE_OPTIONS, JWT_COOKIE_NAME } from "../../config";

export const logout = (_req: Request, res: Response) => {
  res.clearCookie(JWT_COOKIE_NAME, COOKIE_OPTIONS);

  return res.json({
    success: true,
    message: "Logged out",
  });
};
