import { scorePrecedent } from "./precedentEngine";
import { conflictAnalysis } from "./conflictEngine";
import { getJudgeInsights } from "./judgeAnalyticsEngine";

// ============================================
// 🏛️ DETECT COURT TYPE
// ============================================

const detectCourtType = (cases: any[]) => {
  try {
    const text = JSON.stringify(cases).toUpperCase();

    if (text.includes("SUPREME")) return "supreme";
    if (text.includes("HIGH COURT") || text.includes("HC")) return "high";
    if (text.includes("TRIBUNAL")) return "tribunal";

    return "general";
  } catch {
    return "general";
  }
};

// ============================================
// ⚖️ APPLY COURT BEHAVIOR
// ============================================

const applyCourtBehavior = (probability: number, court: string) => {
  if (court === "supreme") return probability - 15;
  if (court === "tribunal") return probability + 10;
  return probability;
};

// ============================================
// 🧠 COURT-SPECIFIC REASONING
// ============================================

const buildCourtReasoning = (base: string, court: string) => {
  if (court === "supreme") {
    return `
SUPREME COURT ANALYSIS:

The Supreme Court applies strict scrutiny and relies heavily on binding precedents.

${base}

The case must demonstrate substantial legal error or miscarriage of justice.
`;
  }

  if (court === "high") {
    return `
HIGH COURT ANALYSIS:

The High Court balances legal principles with factual evaluation.

${base}

Relief depends on both law and factual matrix.
`;
  }

  if (court === "tribunal") {
    return `
TRIBUNAL ANALYSIS:

The Tribunal focuses more on procedural and factual justice.

${base}

Greater flexibility is applied compared to constitutional courts.
`;
  }

  return base;
};

// ============================================
// ⚖️ AI JUDGE DECISION ENGINE (FINAL)
// ============================================

export const generateJudgeDecision = async (
  cases: any[],
  query: string
) => {
  try {
    if (!cases || !cases.length) {
      return {
        successProbability: 0,
        reasoning: "No relevant precedents found.",
        decision: "Insufficient data",
        courtType: "unknown",
        judgeInsights: null,
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
      (scored.length || 1);

    let probability = Math.round(avgScore * 5);

    // Normalize
    probability = Math.min(90, Math.max(20, probability));

    // ==========================================
    // ⚖️ CONFLICT ANALYSIS
    // ==========================================
    const conflicts = conflictAnalysis(cases) || {};

    if (conflicts?.conflicts?.length) {
      probability -= 20;
    }

    if (conflicts?.overruling?.length) {
      probability -= 30;
    }

    // ==========================================
    // 🏛️ COURT BEHAVIOR
    // ==========================================
    const courtType = detectCourtType(cases);

    probability = applyCourtBehavior(probability, courtType);

    // ==========================================
    // 🧠 JUDGE ANALYTICS (NEW)
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

    // Clamp final
    probability = Math.max(10, Math.min(95, probability));

    // ==========================================
    // 🧠 BASE REASONING
    // ==========================================
    const baseReasoning = `
• Average precedent strength: ${avgScore.toFixed(2)}
• Conflicting judgments: ${conflicts?.conflicts?.length || 0}
• Overruled risks: ${conflicts?.overruling?.length || 0}
• Judge success rate: ${judgeInsights?.successRate ?? "N/A"}%
• Bail tendency: ${judgeInsights?.bailTrend ?? "Unknown"}

The probability reflects:
- strength of cited judgments
- consistency in legal reasoning
- presence of conflicting or overruling precedents
- historical judicial tendencies
`;

    const reasoning = buildCourtReasoning(baseReasoning, courtType);

    // ==========================================
    // ⚖️ FINAL DECISION LABEL
    // ==========================================
    let decision = "Balanced Case";

    if (probability > 70) {
      decision = "Likely to Succeed";
    } else if (probability < 40) {
      decision = "Low Chance of Success";
    }

    return {
      courtType,
      successProbability: probability,
      decision,
      reasoning,
      judgeInsights,
    };

  } catch (err) {
    console.error("Judge Engine Error:", err);

    return {
      successProbability: 0,
      decision: "Error",
      reasoning: "Judge analysis failed",
      courtType: "unknown",
      judgeInsights: null,
    };
  }
};
