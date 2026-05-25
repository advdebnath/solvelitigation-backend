import Judgment from "../models/judgment.model";

const clean = (t: string = "") =>
  t.replace(/\s+/g, " ").trim();

// ============================================
// 🔍 EXPLAIN JUDGMENT
// ============================================

export const explainJudgment = async (id: string) => {
  const doc: any = await Judgment.findById(id).lean();

  if (!doc) {
    throw new Error("Judgment not found");
  }

  const text = clean(doc.fullText || "");

  const sentences = text.split(".").map((s) => s.trim());

  // =========================================
  // 🔥 FACTS
  // =========================================
  const facts = sentences.slice(0, 5).join(". ");

  // =========================================
  // 🔥 ISSUE
  // =========================================
  const issue =
    sentences.find((s) =>
      s.toLowerCase().includes("issue")
    ) || "Issue not clearly identified";

  // =========================================
  // 🔥 REASONING
  // =========================================
  const reasoning =
    sentences.find(
      (s) =>
        s.length > 40 &&
        (s.includes("held") ||
          s.includes("observed") ||
          s.includes("considered"))
    ) || "Reasoning not found";

  // =========================================
  // 🔥 DECISION
  // =========================================
  const decision =
    sentences.find(
      (s) =>
        s.toLowerCase().includes("allowed") ||
        s.toLowerCase().includes("dismissed")
    ) || "Decision not clear";

  return {
    caseNumber: doc.caseNumber,
    facts,
    issue,
    reasoning,
    decision,
    pointsOfLaw: doc.pointsOfLaw || [],
  };
};
