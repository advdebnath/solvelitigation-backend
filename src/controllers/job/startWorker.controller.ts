import { Request, Response } from "express";
import { planExpiryWorker } from "@/workers";

export async function startWorker(req: Request, res: Response) {
  try {
    await planExpiryWorker();
    return res.json({
      success: true,
      message: "Plan expiry worker executed successfully",
    });
  } catch (error) {
    console.error("[WORKER START ERROR]", error);
    return res.status(500).json({
      success: false,
      message: "Worker execution failed",
    });
  }
}
