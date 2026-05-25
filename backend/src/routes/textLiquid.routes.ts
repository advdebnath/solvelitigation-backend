import { Router } from "express";
import Judgment from "../models/judgment.model";

const router = Router();

// ============================================
// 🔥 SAFE REGEX BUILDER
// ============================================
const escapeRegex = (text: string) =>
  text.replace(/[.*+?^${}()|[\]\\]/g, "\\$&");

// ============================================
// 🔥 KEYWORD EXTRACTOR (COMMON)
// ============================================
const extractKeywords = (text: string): string[] => {
  return text
    .toLowerCase()
    .replace(/[^a-z0-9\s]/g, "")
    .split(" ")
    .filter((w: string) => w.length > 3)
    .slice(0, 10);
};

// ============================================
// 🔥 SCORE FUNCTION (COMMON)
// ============================================
const calculateScore = (text: string, keywords: string[]) => {
  let score = 0;
  const lower = text.toLowerCase();

  keywords.forEach((k) => {
    if (lower.includes(k)) score += 2;
  });

  return score;
};

// ============================================
// 🔥 FETCH + SCORE ENGINE (COMMON CORE)
// ============================================
const fetchAndRank = async (keywords: string[]) => {
  const regex = keywords.map(escapeRegex).join("|");

  const raw = await Judgment.find({
    fullText: { $regex: regex, $options: "i" },
  })
    .select("_id citation headnote acts sections pointOfLaw fullText")
    .limit(30);

  const scored = raw.map((j) => {
    const score = calculateScore(j.fullText || "", keywords);

    return {
      _id: j._id,
      citation: j.citation,
      headnote: j.headnote,
      acts: j.acts,
      sections: j.sections,
      pointOfLaw: j.pointOfLaw,
      score,
    };
  });

  const matches = scored
    .sort((a, b) => b.score - a.score)
    .slice(0, 10);

  const bestMatch = matches[0] || null;

  return { matches, bestMatch };
};

// ============================================
// 🔥 INSIGHTS BUILDER (COMMON)
// ============================================
const buildInsights = (matches: any[]) => {
  const acts = [...new Set(matches.flatMap((j) => j.acts || []))];
  const sections = [...new Set(matches.flatMap((j) => j.sections || []))];
  const points = [
    ...new Set(matches.map((j) => j.pointOfLaw).filter(Boolean)),
  ];

  return { acts, sections, points };
};

// ============================================
// 🔥 BASIC TEXT LIQUID (ANALYZE)
// ============================================
router.post("/analyze", async (req, res) => {
  try {
    console.log("🔥 TEXT LIQUID ANALYZE HIT");

    const { text } = req.body;

    if (!text || text.length < 5) {
      return res.status(400).json({
        success: false,
        message: "Invalid input text",
      });
    }

    const keywords = extractKeywords(text);

    if (!keywords.length) {
      return res.json({
        success: true,
        data: {
          count: 0,
          bestMatch: null,
          matches: [],
          insights: {},
        },
      });
    }

    const { matches, bestMatch } = await fetchAndRank(keywords);
    const insights = buildInsights(matches);

    res.json({
      success: true,
      data: {
        count: matches.length,
        bestMatch,
        matches,
        insights,
      },
    });

  } catch (err) {
    console.error("❌ Text Liquid Analyze Error:", err);
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 ADVANCED TEXT LIQUID ENGINE
// ============================================
router.post("/advanced", async (req, res) => {
  try {
    console.log("🔥 TEXT LIQUID ADVANCED HIT");

    const { text } = req.body;

    if (!text || text.length < 5) {
      return res.status(400).json({ success: false });
    }

    const keywords = extractKeywords(text);

    if (!keywords.length) {
      return res.json({ success: true, data: {} });
    }

    const { matches, bestMatch } = await fetchAndRank(keywords);

    // ===============================
    // 🔹 SIMILAR CASES
    // ===============================
    let similarCases: any[] = [];

    if (bestMatch?.pointOfLaw) {
      similarCases = await Judgment.find({
        pointOfLaw: bestMatch.pointOfLaw,
        _id: { $ne: bestMatch._id },
      })
        .select("_id citation headnote")
        .limit(5);
    }

    // ===============================
    // 🔹 ARGUMENT BUILDER
    // ===============================
    const argument = bestMatch
      ? `In view of ${bestMatch.citation}, the issue regarding "${bestMatch.pointOfLaw}" is governed by the principle that ${bestMatch.headnote}.`
      : null;

    // ===============================
    // 🔹 REASONING
    // ===============================
    const reasoning = bestMatch
      ? `Match found based on keywords: ${keywords.join(", ")}`
      : "No strong match found";

    const insights = buildInsights(matches);

    res.json({
      success: true,
      data: {
        bestMatch,
        matches,
        similarCases,
        argument,
        reasoning,
        insights,
      },
    });

  } catch (err) {
    console.error("❌ Advanced Text Liquid Error:", err);
    res.status(500).json({ success: false });
  }
});

export default router;
