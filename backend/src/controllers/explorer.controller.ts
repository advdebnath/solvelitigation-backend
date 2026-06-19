import { Request, Response } from "express";

import Judgment from "../models/judgment.model";

// ============================================================
// 🔥 RBAC FILTER
// ============================================================

const applyRBAC = (

  req: any,

  baseFilter: any

) => {

  if (

    !["superadmin", "editor"]
      .includes(req.user?.role)

  ) {

    return {

      ...baseFilter,

      status: "APPROVED",

        isExplorerVisible: true
    };
  }

  return baseFilter;
};

// ============================================================
// 🔥 CATEGORY → ACTS
// ============================================================

export const getByCategory = async (

  req: Request,

  res: Response

) => {

  try {

    const category =
      decodeURIComponent(
        req.params.category
      );

    const filter =
      applyRBAC(req, {

        category
      });

    // ======================================================
    // 🔥 ACT AGGREGATION
    // ======================================================

    const acts =
      await Judgment.aggregate([

        {
          $match: filter
        },

        {
          $unwind: "$actNames"
        },

        {
          $group: {

            _id: "$actNames",

            count: {
              $sum: 1
            }
          }
        },

        {
          $project: {

            _id: 0,

            act: "$_id",

            count: 1
          }
        },

        {
          $sort: {

            count: -1,

            act: 1
          }
        },

        {
          $limit: 100
        }
      ]);

    return res.json({

      success: true,

      category,

      totalActs:
        acts.length,

      data: acts
    });

  } catch (err) {

    console.error(
      "❌ Explorer Category Error:",
      err
    );

    return res.status(500).json({

      success: false,

      message:
        "Failed to fetch acts"
    });
  }
};

// ============================================================
// 🔥 ACT → POINTS OF LAW
// ============================================================

export const getByAct = async (

  req: Request,

  res: Response

) => {

  try {

    const act =
      decodeURIComponent(
        req.params.act
      );

    const filter =
      applyRBAC(req, {

        actNames: act
      });

    // ======================================================
    // 🔥 POINT AGGREGATION
    // ======================================================

    const points =
      await Judgment.aggregate([

        {
          $match: filter
        },

        {
          $unwind: "$pointsOfLaw"
        },

        {
          $group: {

            _id:
              "$pointsOfLaw.point",

            count: {

              $sum: 1
            }
          }
        },

        {
          $project: {

            _id: 0,

            point: "$_id",

            count: 1
          }
        },

        {
          $sort: {

            count: -1,

            point: 1
          }
        },

        {
          $limit: 100
        }
      ]);

    return res.json({

      success: true,

      act,

      totalPoints:
        points.length,

      data: points
    });

  } catch (err) {

    console.error(
      "❌ Explorer Act Error:",
      err
    );

    return res.status(500).json({

      success: false,

      message:
        "Failed to fetch points"
    });
  }
};

// ============================================================
// 🔥 SECTION → JUDGMENTS
// ============================================================

export const getBySection = async (

  req: Request,

  res: Response

) => {

  try {

    const section =
      decodeURIComponent(
        req.params.section
      );

    const filter =
      applyRBAC(req, {

        "sections.section":
          section
      });

    const judgments =
      await Judgment.find(filter)

        .select(`

          caseNumber
          category
          court
          headnote
          sections
          judgmentDate
        `)

        .sort({

          judgmentDate: -1
        })

        .limit(100)

        .lean();

    return res.json({

      success: true,

      section,

      total:
        judgments.length,

      data: judgments
    });

  } catch (err) {

    console.error(
      "❌ Explorer Section Error:",
      err
    );

    return res.status(500).json({

      success: false,

      message:
        "Failed to fetch section judgments"
    });
  }
};

// ============================================================
// 🔥 POINT → JUDGMENTS
// ============================================================

export const getByPoint = async (

  req: Request,

  res: Response

) => {

  try {

    const point =
      decodeURIComponent(
        req.params.point
      );

    const filter =
      applyRBAC(req, {

        "pointsOfLaw.point":
          point
      });

    const judgments =
      await Judgment.find(filter)

        .select(`

          caseNumber
          headnote
          category
          court
          actNames
          judgmentDate
        `)

        .sort({

          judgmentDate: -1
        })

        .limit(100)

        .lean();

    return res.json({

      success: true,

      point,

      total:
        judgments.length,

      data: judgments
    });

  } catch (err) {

    console.error(
      "❌ Explorer Point Error:",
      err
    );

    return res.status(500).json({

      success: false,

      message:
        "Failed to fetch judgments"
    });
  }
};

// ============================================================
// 🔥 JUDGMENT VIEW
// ============================================================

export const getJudgmentById =
  async (

    req: Request,

    res: Response

  ) => {

    try {

      const id =
        req.params.id;

      const filter: any = {
  _id: id
};

if (
  !["superadmin", "editor"]
    .includes((req as any).user?.role)
) {

  filter.isExplorerVisible = true;
}

const judgment =
  await Judgment.findOne(filter)
    .lean();

      if (!judgment) {

        return res
          .status(404)
          .json({

            success: false,

            message:
              "Judgment not found"
          });
      }

      return res.json({

        success: true,

        data: judgment
      });

    } catch (err) {

      console.error(
        "❌ Explorer Judgment Error:",
        err
      );

      return res.status(500).json({

        success: false,

        message:
          "Failed to fetch judgment"
      });
    }
  };
