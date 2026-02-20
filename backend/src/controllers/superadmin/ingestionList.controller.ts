import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";

export const listIngestions = async (req: Request, res: Response) => {
  try {
    const { page = 1, limit = 20, status } = req.query;

    const query: any = {};
    if (status) {
      query.status = status;
    }

    const ingestions = await JudgmentIngestion.find(query)
      .sort({ createdAt: -1 })
      .skip((Number(page) - 1) * Number(limit))
      .limit(Number(limit))
      .select(
        "file.originalName status retryCount error createdAt permanentFailureAt"
      );

    const total = await JudgmentIngestion.countDocuments(query);

    return res.json({
      success: true,
      total,
      page: Number(page),
      pages: Math.ceil(total / Number(limit)),
      data: ingestions,
    });
  } catch (err) {
    console.error("List ingestions error:", err);
    return res.status(500).json({ message: "Failed to list ingestions" });
  }
};
