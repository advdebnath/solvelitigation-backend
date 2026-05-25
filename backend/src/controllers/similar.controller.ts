import { Request, Response } from "express";
import mongoose from "mongoose";
import Judgment from "../models/judgment.model";

/* ---------------------------------------------------- */
/* 🔹 Utility Functions */
/* ---------------------------------------------------- */

const tokenize = (text: string): string[] => {
  return (text || "")
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, " ")
    .split(/\s+/)
    .filter(Boolean);
};

const overlapScore = (a: string[], b: string[]): number => {
  if (!a.length || !b.length) return 0;

  const setA = new Set(a);
  const setB = new Set(b);

  let intersection = 0;
  setA.forEach((t) => {
    if (setB.has(t)) intersection++;
  });

  const union = new Set([...a, ...b]).size || 1;
  return intersection / union;
};

/* ---------------------------------------------------- */
/* 🔥 Controller */
/* ---------------------------------------------------- */

export const getSimilarCases = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    /* ---------------- VALIDATION ---------------- */
    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({
        success: false,
        message: "Invalid case id",
      });
    }

    const objectId = new mongoose.Types.ObjectId(id);

    /* ---------------- BASE CASE ---------------- */
    const base = await Judgment.findById(objectId).lean();

    if (!base) {
      return res.status(404).json({
        success: false,
        message: "Case not found",
      });
    }

    const baseCase = base as any;

    const baseCategory: string = baseCase.category || "";
    const basePoints: string[] = baseCase.pointsOfLaw || [];
    const baseActs: string[] = (baseCase.actReferences || []).map((x: any) =>
      String(x)
    );
    const baseHeadTokens: string[] = tokenize(baseCase.headnote || "");

    /* ---------------- FETCH CANDIDATES ---------------- */
    const candidatesRaw = await Judgment.find({
      _id: { $ne: objectId },
      $or: [
        { category: baseCategory },
        { pointsOfLaw: { $in: basePoints } },
        { actReferences: { $in: baseCase.actReferences || [] } },
      ],
    })
      .select("_id caseNumber court category pointsOfLaw actReferences headnote")
      .limit(200)
      .lean();

    const candidates = candidatesRaw as any[];

    /* ---------------- SCORING ---------------- */
    const scored = candidates.map((c) => {
      let score = 0;

      const cPoints: string[] = c.pointsOfLaw || [];
      const cActs: string[] = (c.actReferences || []).map((x: any) =>
        String(x)
      );
      const cHeadTokens: string[] = tokenize(c.headnote || "");

      /* 🔥 Points Match (Strong) */
      const pointMatches = cPoints.filter((p) => basePoints.includes(p)).length;
      if (pointMatches > 0) score += 5 + pointMatches;

      /* 🔥 Headnote Similarity */
      const headSim = overlapScore(baseHeadTokens, cHeadTokens);
      if (headSim > 0) score += Math.round(headSim * 4);

      /* 🔥 Act Match */
      const actMatches = cActs.filter((a) => baseActs.includes(a)).length;
      if (actMatches > 0) score += 2 + actMatches;

      /* 🔥 Category Match */
      if (c.category === baseCategory) score += 1;

      return {
        _id: c._id,
        caseNumber: c.caseNumber,
        court: c.court,
        category: c.category,
        pointsOfLaw: c.pointsOfLaw || [],
        score,
      };
    });

    let similar = scored
      .filter((x) => x.score > 0)
      .sort((a, b) => b.score - a.score)
      .slice(0, 10);

    /* ---------------- FALLBACK ---------------- */
    if (similar.length === 0) {
      const fallback = await Judgment.find({ _id: { $ne: objectId } })
        .select("_id caseNumber court category pointsOfLaw")
        .limit(5)
        .lean();

      similar = fallback.map((f: any) => ({
        _id: f._id,
        caseNumber: f.caseNumber,
        court: f.court,
        category: f.category,
        pointsOfLaw: f.pointsOfLaw || [],
        score: 0,
      }));
    }

    /* ---------------- RESPONSE ---------------- */
    return res.json({
      success: true,
      baseCase: {
        _id: baseCase._id,
        caseNumber: baseCase.caseNumber,
        category: baseCase.category,
      },
      count: similar.length,
      similar,
    });

  } catch (error) {
    console.error("❌ Similar case error:", error);

    return res.status(500).json({
      success: false,
      message: "Failed to fetch similar cases",
    });
  }
};
