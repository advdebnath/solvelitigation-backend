import { Request, Response } from "express";
import Judgment from "../models/judgment.model";

export const getJudgmentFilters = async (
  _req: Request,
  res: Response
) => {
  try {
    const aggregation = await Judgment.aggregate([
      {
        $facet: {
          courtTypes: [
            { $match: { courtType: { $exists: true, $ne: null } } },
            {
              $group: {
                _id: "$courtType",
                count: { $sum: 1 },
              },
            },
            { $sort: { _id: 1 } },
          ],
          years: [
            { $match: { year: { $exists: true, $ne: null } } },
            {
              $group: {
                _id: "$year",
                count: { $sum: 1 },
              },
            },
            { $sort: { _id: -1 } },
          ],
          categories: [
            { $match: { category: { $exists: true, $ne: null } } },
            {
              $group: {
                _id: "$category",
                count: { $sum: 1 },
              },
            },
            { $sort: { _id: 1 } },
          ],
          total: [
            { $count: "count" }
          ],
        },
      },
    ]);

    const result = aggregation[0];

    return res.json({
      success: true,
      data: {
        courtTypes: result.courtTypes.map((c: any) => ({
          value: c._id,
          count: c.count,
        })),
        years: result.years.map((y: any) => ({
          value: y._id,
          count: y.count,
        })),
        categories: result.categories.map((cat: any) => ({
          value: cat._id,
          count: cat.count,
        })),
        totalJudgments: result.total[0]?.count || 0,
      },
    });
  } catch (error) {
    console.error("Filter Metadata Error:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch filter metadata",
    });
  }
};
