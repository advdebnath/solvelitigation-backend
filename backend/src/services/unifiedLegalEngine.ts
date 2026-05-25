import { scorePrecedent } from "./precedentEngine";
import { conflictAnalysis } from "./conflictEngine";
import { getJudgeInsights } from "./judgeAnalyticsEngine";

// ============================================
// 🧠 UNIFIED LEGAL SCORING ENGINE
// ============================================

export const unifiedLegalAnalysis = async (
  cases: any[],
  query: string
) => {
  try {
    if (!cases || !cases.length) {
      return {
        successProbability: 0,
        decision: "No Data",
        reasoning: "No cases available",
      };
    }

    // ==========================================
    // 🔥 PRECEDENT SCORING
    // ==========================================
    const scored = cases.map((c) => ({
      ...c,
      score: scorePrecedent(c),
    }));

    const avgScore =
      scored.reduce((sum, c) => sum + (c.score || 0), 0) /
      scored.length;

    let probability = avgScore * 5;

    // ==========================================
    // ⚖️ CONFLICT ANALYSIS
    // ==========================================
    const conflicts = conflictAnalysis(cases);

    if (conflicts?.overruling?.length) {
      probability -= 25;
    }

    if (conflicts?.conflicts?.length) {
      probability -= 15;
    }

    if (conflicts?.distinguishing?.length) {
      probability -= 5;
    }

    if (
      (conflicts?.supporting?.length || 0) >
      (conflicts?.conflicts?.length || 0)
    ) {
      probability += 10;
    }

    // ==========================================
    // 🧠 JUDGE ANALYTICS
    // ==========================================
    const judgeInsights = await getJudgeInsights(cases);

    if (judgeInsights) {
      if (judgeInsights.successRate < 40) {
        probability -= 10;
      }

      if (judgeInsights.bailTrend === "Conservative") {
        probability -= 5;
      }
    }

    // ==========================================
    // 🏛️ COURT DETECTION
    // ==========================================
    const text = JSON.stringify(cases).toUpperCase();

    let courtType = "general";

    if (text.includes("SUPREME")) courtType = "supreme";
    else if (text.includes("HIGH COURT")) courtType = "high";
    else if (text.includes("TRIBUNAL")) courtType = "tribunal";

    if (courtType === "supreme") probability -= 10;
    if (courtType === "tribunal") probability += 10;

    // ==========================================
    // 🔒 CLAMP
    // ==========================================
    probability = Math.max(10, Math.min(95, Math.round(probability)));

    // ==========================================
    // ⚖️ DECISION LABEL
    // ==========================================
    let decision = "Balanced Case";

    if (probability > 70) decision = "Likely to Succeed";
    else if (probability < 40) decision = "Low Chance";

    // ==========================================
    // 🧠 REASONING
    // ==========================================
    const reasoning = `
• Avg Precedent Score: ${avgScore.toFixed(2)}
• Conflicts: ${conflicts?.conflicts?.length || 0}
• Overruling: ${conflicts?.overruling?.length || 0}
• Supporting: ${conflicts?.supporting?.length || 0}
• Judge Success Rate: ${judgeInsights?.successRate ?? "N/A"}%

Final probability considers:
- hierarchy of courts
- consistency of precedents
- judicial behavior trends
`;

    return {
      successProbability: probability,
      decision,
      courtType,
      judgeInsights,
      conflicts,
      reasoning,
    };

  } catch (err) {
    console.error("Unified Engine Error:", err);

    return {
      successProbability: 0,
      decision: "Error",
      reasoning: "Unified analysis failed",
    };
  }
};
