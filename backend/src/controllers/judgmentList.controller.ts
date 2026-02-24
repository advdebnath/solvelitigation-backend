import { Request, Response } from "express";
import Judgment from "../models/judgment.model";
import { redisClient } from "../config/redis";

const CACHE_TTL = 60 * 3; // 3 minutes

export const listJudgments = async (req: Request, res: Response) => {
  try {
    const page = parseInt(req.query.page as string) || 1;
    const limit = parseInt(req.query.limit as string) || 10;

    const search = (req.query.search as string) || "";
    const courtType = (req.query.courtType as string) || "";
    const year = req.query.year ? parseInt(req.query.year as string) : "";
    const category = (req.query.category as string) || "";

    const skip = (page - 1) * limit;

    const filter: any = {};

    if (courtType) filter.courtType = courtType;
    if (year) filter.year = year;
    if (category) filter.category = category;

    if (search) {
      filter.$text = { $search: search };
    }

    /* ---------------- CACHE KEY ---------------- */
    const cacheKey = `judgments:list:${page}:${limit}:${search}:${courtType}:${year}:${category}`;

    /* ---------------- CHECK CACHE ---------------- */
    const cached = await redisClient.get(cacheKey);
    if (cached) {
      return res.json(JSON.parse(cached));
    }

    /* ---------------- QUERY DB ---------------- */
    const [judgments, total] = await Promise.all([
      Judgment.find(
        filter,
        search ? { score: { $meta: "textScore" } } : {}
      )
        .sort(
          search
            ? { score: { $meta: "textScore" } }
            : { createdAt: -1 }
        )
        .skip(skip)
        .limit(limit)
        .select(
          "caseNumber category court confidence judgmentDate nlpStatus pageCount createdAt"
        ),
      Judgment.countDocuments(filter),
    ]);

    const responseData = {
      success: true,
      data: judgments,
      pagination: {
        total,
        page,
        pages: Math.ceil(total / limit),
        limit,
      },
    };

    /* ---------------- STORE CACHE ---------------- */
    await redisClient.set(cacheKey, JSON.stringify(responseData), {
      EX: CACHE_TTL,
    });

    return res.json(responseData);
  } catch (error) {
    console.error("List Judgments Error:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch judgments",
    });
  }
};
