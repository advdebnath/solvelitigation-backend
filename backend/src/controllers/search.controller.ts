import { Request, Response } from "express";
import axios from "axios";
import Judgment from "../models/judgment.model";

// ============================================
// 🔍 HYBRID SEARCH (FINAL PRODUCTION SAFE)
// ============================================
export const searchJudgments = async (req: Request, res: Response) => {
  try {
    const q = String(req.query.q || "").trim();
    const category = req.query.category as string;
    const court = req.query.court as string;

    const page = Math.max(Number(req.query.page || 1), 1);
    const limit = Math.min(Number(req.query.limit || 20), 50);

    // ============================================
    // 🔥 VALIDATION
    // ============================================
    if (!q && !category && !court) {
      return res.status(400).json({
        success: false,
        message: "At least one filter (q, category, court) is required",
      });
    }

    let semanticResults: any[] = [];
    let dbResults: any[] = [];

    // ============================================
    // 🔥 1. SEMANTIC SEARCH
    // ============================================
    if (q) {
      try {
        const { data } = await axios.post(
          "http://127.0.0.1:8000/api/semantic/search",
          { query: q }
        );

        semanticResults = data?.results || [];
      } catch (err) {
        console.warn("⚠️ NLP unavailable, fallback to DB search");
      }
    }

    // ============================================
    // 🔥 2. DB FILTER
    // ============================================
    let filter: any = {};

    if (q) {
      const safeQ = q.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

      filter.$or = [
        { caseNumber: { $regex: safeQ, $options: "i" } },
        { headnote: { $regex: safeQ, $options: "i" } },
        { pointsOfLaw: { $regex: safeQ, $options: "i" } }
      ];
    }

    // ✅ FIXED CATEGORY MATCH (CASE-INSENSITIVE EXACT)
    if (category) {
      const safeCategory = category.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      filter.category = { $regex: `^${safeCategory}$`, $options: "i" };
    }

    // ✅ FIXED COURT MATCH
    if (court) {
      const safeCourt = court.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");
      filter.court = { $regex: `^${safeCourt}$`, $options: "i" };
    }

    // ============================================
    // 🔥 FETCH DB DATA
    // ============================================
    const total = await Judgment.countDocuments(filter);

    const raw = await Judgment.find(filter)
      .select("_id caseNumber court category headnote pointsOfLaw")
      .skip((page - 1) * limit)
      .limit(limit)
      .lean();

    // ============================================
    // 🔥 SCORING
    // ============================================
    if (q) {
      const words = q.toLowerCase().split(/\s+/);

      dbResults = raw.map((doc: any) => {
        let score = 0;

        const text = `${doc.pointsOfLaw?.join(" ")} ${doc.headnote}`.toLowerCase();

        for (const word of words) {
          if (text.includes(word)) score += 2;
          if (doc.caseNumber?.toLowerCase().includes(word)) score += 1;
        }

        return { ...doc, score };
      });

      dbResults.sort((a, b) => b.score - a.score);
    } else {
      dbResults = raw;
    }

    // ============================================
    // 🔥 MERGE RESULTS
    // ============================================
    const combined = [...semanticResults, ...dbResults];

    const uniqueMap = new Map();
    combined.forEach((item) => {
      if (item._id && !uniqueMap.has(item._id)) {
        uniqueMap.set(item._id, item);
      }
    });

    const results = Array.from(uniqueMap.values());

    return res.json({
      success: true,
      query: q || null,
      page,
      limit,
      total,
      count: results.length,
      results,
    });

  } catch (err) {
    console.error("❌ Search Error:", err);
    return res.status(500).json({
      success: false,
      message: "Search failed",
    });
  }
};
