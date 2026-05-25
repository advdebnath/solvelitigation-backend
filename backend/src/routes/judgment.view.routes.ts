import express, { Request, Response } from "express";
import Judgment from "../models/judgment.model";

// 🔥 PRECEDENT ENGINE
import { findPrecedents } from "../services/precedentEngine";

const router = express.Router();

// ============================================
// 🔥 OPEN JUDGMENT + RELATED + PRECEDENTS
// ============================================

router.get("/:id", async (req: Request, res: Response) => {
  try {
    // 🔥 FIX: FORCE SINGLE OBJECT TYPE
    const judgment = (await Judgment.findById(req.params.id).lean()) as any;

    if (!judgment) {
      return res.status(404).json({
        success: false,
        message: "Judgment not found",
      });
    }

    // ============================================
    // 🔥 SAFE FIELD EXTRACTION
    // ============================================

    const category = judgment.category || "Unknown";
    const pointOfLaw: string[] = judgment.pointOfLaw || [];

    // ============================================
    // 🔥 RELATED CASES (FIXED FIELD NAME)
    // ============================================

    const related = await Judgment.find({
      _id: { $ne: judgment._id },
      category,

      // 🔥 Only apply if exists
      ...(pointOfLaw.length > 0 && {
        pointOfLaw: { $in: pointOfLaw },
      }),
    })
      .sort({ judgmentDate: -1 }) // latest first
      .limit(5)
      .select("caseNumber slscCitation judgmentDate")
      .lean();

    // ============================================
    // 🔥 PRECEDENT ENGINE (ADVANCED)
    // ============================================

    const precedents = await findPrecedents(judgment);

    // ============================================
    // 🔥 RESPONSE
    // ============================================

    return res.json({
      success: true,

      data: judgment,

      // 🔥 RELATED CASES
      relatedCases: related.map((r: any) => ({
        id: r._id,

        display: r.slscCitation
          ? `${r.slscCitation} (${r.caseNumber})`
          : r.caseNumber,

        date: r.judgmentDate || null,

        url: `/api/judgment/${r._id}`,
      })),

      // 🔥 PRECEDENTS (CORE FEATURE)
      precedents,
    });
  } catch (err) {
    console.error("Judgment View Error:", err);

    return res.status(500).json({
      success: false,
      message: "Server error",
    });
  }
});

export default router;
