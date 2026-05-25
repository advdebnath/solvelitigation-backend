import { Request, Response } from "express";
import Act from "../models/actMaster.model";

// ==========================================================
// 🔥 GET ACTS BY CATEGORY
// ==========================================================

export const getActsByCategory = async (
  req: Request,
  res: Response
) => {

  try {

    const { category } = req.query;

    // ======================================================
    // 🔥 VALIDATION
    // ======================================================

    if (!category) {

      return res.status(400).json({

        success: false,

        message: "Category is required"
      });
    }

    // ======================================================
    // 🔥 FETCH CATEGORY ACTS
    // ======================================================

    /**
     * IMPORTANT:
     *
     * Older act documents do not contain
     * category field.
     *
     * Therefore:
     *
     * - include matching category acts
     * - also include legacy uncategorized acts
     */

    const acts = await Act.find({

      $or: [

        {
          category: String(category)
        },

        {
          category: {
            $exists: false
          }
        }
      ]

    })

    .sort({
      canonicalName: 1
    })

    .lean();

    // ======================================================
    // 🔥 RESPONSE
    // ======================================================

    return res.status(200).json({

      success: true,

      category,

      total: acts.length,

      acts
    });

  } catch (error: any) {

    console.error(
      "❌ getActsByCategory error:",
      error
    );

    return res.status(500).json({

      success: false,

      message: "Internal server error",

      error:
        process.env.NODE_ENV !== "production"
          ? error?.message
          : undefined
    });
  }
};
