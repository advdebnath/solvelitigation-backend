import Judgment from "../models/judgment.model";

// ============================================
// 🧠 MULTI CASE REASONING ENGINE
// ============================================

export const multiCaseReasoning = async (cases: any[], query: string) => {
  const issues: string[] = [];
  const findings: string[] = [];
  const reasoning: string[] = [];

  cases.forEach((c) => {
    const text = (c.fullText || "").toLowerCase();

    if (text.includes("issue")) {
      issues.push(`Issue considered in ${c.caseNumber}`);
    }

    if (text.includes("held") || text.includes("observed")) {
      findings.push(`Court in ${c.caseNumber} made key findings`);
    }

    const important = (c.fullText || "")
      .split(".")
      .map((s: string) => s.trim())
      .find(
        (s: string) =>
          s.length > 40 &&
          (s.includes("proved") ||
            s.includes("not proved") ||
            s.includes("evidence") ||
            s.includes("doubt"))
      );

    if (important) {
      reasoning.push(`${c.caseNumber}: ${important}`);
    }
  });

  return {
    issues,
    findings,
    reasoning,
  };
};

// ============================================
// ⚖️ JUDGE SIMULATION ENGINE
// ============================================

export const judgeSimulation = async (cases: any[], query: string) => {
  const reasoningBlock = await multiCaseReasoning(cases, query);

  return {
    court: "Simulated Court of Law",

    issue:
      reasoningBlock.issues[0] ||
      "Issue: Whether the prosecution has proved the case beyond reasonable doubt",

    analysis: reasoningBlock.reasoning,

    findings: reasoningBlock.findings,

    decision:
      reasoningBlock.reasoning.length > 2
        ? "Based on the above reasoning, the case leans in favour of conviction."
        : "Benefit of doubt goes to the accused.",

    conclusion:
      "The case must be decided based on cumulative evaluation of evidence.",
  };
};
