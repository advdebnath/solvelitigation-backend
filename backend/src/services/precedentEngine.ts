import Judgment from "../models/judgment.model";

// ============================================
// ⚖️ COURT WEIGHT (HIERARCHY)
// ============================================

export const getCourtWeight = (caseNumber: string = "") => {
  const c = (caseNumber || "").toUpperCase();

  if (c.includes("SUPREME")) return 10;
  if (c.includes("HIGH COURT") || c.includes("HC")) return 7;
  if (c.includes("TRIBUNAL")) return 4;

  return 2;
};

// ============================================
// 📅 RECENCY WEIGHT
// ============================================

export const getRecencyWeight = (date?: string) => {
  if (!date) return 1;

  const year = new Date(date).getFullYear();
  if (!year || isNaN(year)) return 1;

  const current = new Date().getFullYear();

  return Math.max(1, 5 - (current - year)); // 1–5
};

// ============================================
// 🔥 PRECEDENT SCORING (FINAL)
// ============================================

export const scorePrecedent = (c: any) => {
  let score = 0;

  // 🔥 Court hierarchy (strong weight)
  score += getCourtWeight(c.caseNumber) * 2;

  // 🔥 Recency
  score += getRecencyWeight(c.judgmentDate);

  // 🔥 Structural strength
  if (c.headnote) score += 2;
  if (c.pointsOfLaw?.length) score += 3;

  // 🔥 Reasoning indicators
  const text = (c.fullText || "").toLowerCase();

  if (text.includes("ratio")) score += 4;
  if (text.includes("held")) score += 3;
  if (text.includes("observed")) score += 2;

  return score;
};

// ============================================
// 🔥 APPLY RANKING
// ============================================

export const rankPrecedents = (cases: any[]) => {
  return (cases || [])
    .map((c) => ({
      ...c,
      precedentScore: scorePrecedent(c),
      courtLevel:
        c.caseNumber?.toUpperCase().includes("SUPREME")
          ? "Supreme Court"
          : c.caseNumber?.toUpperCase().includes("HIGH")
          ? "High Court"
          : c.caseNumber?.toUpperCase().includes("TRIBUNAL")
          ? "Tribunal"
          : "Other",
    }))
    .sort((a, b) => b.precedentScore - a.precedentScore);
};

// ============================================
// 🔥 PRECEDENT ENGINE (UPGRADED)
// ============================================

export const findPrecedents = async (judgment: any) => {
  try {
    const { category, pointsOfLaw = [] } = judgment;

    // =========================================
    // 🔥 SIMILAR CASES
    // =========================================
    let similar = await Judgment.find({
      _id: { $ne: judgment._id },
      category,
      pointsOfLaw: { $in: pointsOfLaw },
    })
      .limit(10)
      .select("caseNumber slscCitation pointsOfLaw headnote fullText judgmentDate")
      .lean();

    // =========================================
    // 🔥 SUPPORTING CASES
    // =========================================
    let supporting = await Judgment.find({
      _id: { $ne: judgment._id },
      category,
      pointsOfLaw: { $all: pointsOfLaw.slice(0, 2) },
    })
      .limit(5)
      .select("caseNumber slscCitation pointsOfLaw headnote fullText judgmentDate")
      .lean();

    // =========================================
    // 🔥 DISTINGUISHING CASES
    // =========================================
    let distinguishing = await Judgment.find({
      _id: { $ne: judgment._id },
      category,
      pointsOfLaw: { $nin: pointsOfLaw },
    })
      .limit(5)
      .select("caseNumber slscCitation pointsOfLaw headnote fullText judgmentDate")
      .lean();

    // =========================================
    // 🔥 APPLY RANKING
    // =========================================
    similar = rankPrecedents(similar);
    supporting = rankPrecedents(supporting);
    distinguishing = rankPrecedents(distinguishing);

    // =========================================
    // 🔥 FORMAT OUTPUT
    // =========================================
    const format = (list: any[]) =>
      list.map((c) => ({
        id: c._id,
        display: c.slscCitation
          ? `${c.slscCitation} (${c.caseNumber})`
          : c.caseNumber,
        score: c.precedentScore,
        court: c.courtLevel,
      }));

    return {
      similar: format(similar),
      supporting: format(supporting),
      distinguishing: format(distinguishing),
    };

  } catch (err) {
    console.error("Precedent Engine Error:", err);

    return {
      similar: [],
      supporting: [],
      distinguishing: [],
    };
  }
};
