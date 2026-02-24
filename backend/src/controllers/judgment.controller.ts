import { Request, Response } from "express";
import Judgment from "../models/judgment.model";
import { buildJudgmentQuery } from "../services/judgmentQueryBuilder.service";

export const getAllJudgments = async (req: Request, res: Response) => {
  try {
    const { filter, page, limit, skip, sort } = buildJudgmentQuery(
      req.query as any
    );

    const total = await Judgment.countDocuments(filter);

    const query = Judgment.find(filter)
      .select(
        "caseNumber judgmentDate category court confidence pageCount createdAt nlpStatus"
      )
      .sort(sort)
      .skip(skip)
      .limit(limit)
      .lean();

    if ((req.query as any).search) {
      query.select({ score: { $meta: "textScore" } });
    }

    const judgments = await query;

    return res.json({
      success: true,
      data: judgments,
      pagination: {
        total,
        page,
        totalPages: Math.ceil(total / limit),
        limit,
        hasNextPage: page < Math.ceil(total / limit),
        hasPrevPage: page > 1,
      },
    });
  } catch (error) {
    console.error("Error fetching judgments:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch judgments",
    });
  }
};
