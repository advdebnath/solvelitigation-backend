import { Request, Response } from "express";

export default function logout(_req: Request, res: Response) {
  res.json({ message: "logout ok" });
}
