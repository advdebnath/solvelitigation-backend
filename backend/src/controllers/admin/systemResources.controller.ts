import { Request, Response } from "express";
import os from "os";

export const getSystemResources = async (req: Request, res: Response) => {
  try {
    const totalMem = os.totalmem();
    const freeMem = os.freemem();
    const usedMem = totalMem - freeMem;

    return res.json({
      success: true,
      data: {
        uptime_seconds: os.uptime(),
        memory: {
          total_mb: Math.round(totalMem / 1024 / 1024),
          used_mb: Math.round(usedMem / 1024 / 1024),
          free_mb: Math.round(freeMem / 1024 / 1024),
        },
        cpu_load: os.loadavg(),
        platform: os.platform(),
      },
    });
  } catch (error) {
    return res.status(500).json({ success: false });
  }
};
