import { Request, Response } from "express";

export default function getMe(_req: Request, res: Response) {
  res.json({ user: null });
}
