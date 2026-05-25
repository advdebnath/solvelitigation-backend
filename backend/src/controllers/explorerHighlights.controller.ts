import { Request, Response } from "express";
import Judgment from "../models/judgment.model";

// =========================================================
// 🔥 TYPES
// =========================================================

interface HighlightItem {

  text: string;

  type: string;

  color: string;
}

interface SectionItem {

  section?: string;

  act?: string;

  type?: string;
}

interface PointItem {

  point?: string;

  category?: string;
}

interface JudgmentLean {

  fullText?: string;

  sections?: SectionItem[];

  pointsOfLaw?: (string | PointItem)[];

  headnote?: string;
}

// =========================================================
// 🔥 GET EXPLORER HIGHLIGHTS
// =========================================================

export const getExplorerHighlights = async (

  req: Request,
  res: Response

) => {

  try {

    const id = String(
      req.params.id || ""
    ).trim();

    const section = String(
      req.query.section || ""
    ).trim();

    const point = String(
      req.query.point || ""
    ).trim();

    const query = String(
      req.query.query || ""
    ).trim();

    // =====================================================
    // 🔥 LOAD JUDGMENT
    // =====================================================

    const judgment = await Judgment.findById(id)

      .select(
        "fullText sections pointsOfLaw headnote"
      )

      .lean<JudgmentLean>();

    if (!judgment) {

      return res.status(404).json({

        success: false,

        message: "Judgment not found"
      });
    }

    // =====================================================
    // 🔥 HIGHLIGHTS
    // =====================================================

    const highlights: HighlightItem[] = [];

    // -----------------------------------------------------
    // MANUAL SECTION
    // -----------------------------------------------------

    if (section) {

      highlights.push({

        text: section,

        type: "section",

        color: "yellow"
      });
    }

    // -----------------------------------------------------
    // MANUAL POINT
    // -----------------------------------------------------

    if (point) {

      highlights.push({

        text: point,

        type: "point",

        color: "cyan"
      });
    }

    // -----------------------------------------------------
    // QUERY
    // -----------------------------------------------------

    if (query) {

      highlights.push({

        text: query,

        type: "query",

        color: "lime"
      });
    }

    // =====================================================
    // 🔥 AUTO SECTIONS
    // =====================================================

    const sections = Array.isArray(
      judgment.sections
    )

      ? judgment.sections

      : [];

    for (const s of sections) {

      if (!s?.section) continue;

      highlights.push({

        text: String(s.section),

        type: "auto-section",

        color: "orange"
      });
    }

    // =====================================================
    // 🔥 AUTO POINTS
    // =====================================================

    const points = Array.isArray(
      judgment.pointsOfLaw
    )

      ? judgment.pointsOfLaw

      : [];

    for (const p of points) {

      let value = "";

      if (typeof p === "string") {

        value = p;

      } else if (

        p &&
        typeof p === "object"

      ) {

        value = p.point || "";
      }

      if (!value) continue;

      highlights.push({

        text: value,

        type: "auto-point",

        color: "pink"
      });
    }

    // =====================================================
    // 🔥 DEDUPLICATION
    // =====================================================

    const seen = new Set<string>();

    const finalHighlights = highlights.filter(
      (h) => {

        const key = `${h.type}:${h.text}`;

        if (seen.has(key)) {

          return false;
        }

        seen.add(key);

        return true;
      }
    );

    // =====================================================
    // 🔥 RESPONSE
    // =====================================================

    return res.json({

      success: true,

      total: finalHighlights.length,

      data: finalHighlights
    });

  } catch (err) {

    console.error(
      "❌ Explorer Highlights Error:",
      err
    );

    return res.status(500).json({

      success: false,

      message:
        "Failed to generate highlights"
    });
  }
};
