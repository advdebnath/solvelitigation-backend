import { Request, Response } from "express";
import { Judgment } from "../models/judgment.model";

export const listJudgments = async (req: Request, res: Response) => {
  try {
    const page = Math.max(parseInt(req.query.page as string) || 1, 1);
    const limit = Math.min(parseInt(req.query.limit as string) || 20, 100);
    const skip = (page - 1) * limit;

    // 🔍 Build dynamic filter
    const filter: any = {};

    if (req.query.year) {
      filter.year = Number(req.query.year);
    }

    if (req.query.status) {
      filter.status = String(req.query.status).toUpperCase();
    }

    if (req.query.nlpStatus) {
      filter["nlp.status"] = String(req.query.nlpStatus).toUpperCase();
    }

    if (req.query.category) {
      filter.category = req.query.category;
    }

    if (req.query.subCategory) {
      filter.subCategory = req.query.subCategory;
    }

    const [items, total] = await Promise.all([
      Judgment.find(filter)
        .sort({ uploadedAt: -1 })
        .skip(skip)
        .limit(limit)
        .select({
          title: 1,
          year: 1,
          status: 1,
          category: 1,
          subCategory: 1,
          "nlp.status": 1,
          uploadedAt: 1,
        })
        .lean(),

      Judgment.countDocuments(filter),
    ]);

    return res.json({
      page,
      limit,
      total,
      items,
    });
  } catch (error) {
    console.error("Judgment list error:", error);
    return res.status(500).json({
      message: "Failed to fetch judgments",
    });
  }
};
