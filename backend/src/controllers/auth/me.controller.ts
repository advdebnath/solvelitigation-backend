import { Request, Response } from "express";

export async function me(req: Request, res: Response) {
  const user = req.user || req.currentUser;

  if (!user) {
    return res.status(401).json({ message: "Not authenticated" });
  }

  return res.json({
    success: true,
    user,
  });
}
