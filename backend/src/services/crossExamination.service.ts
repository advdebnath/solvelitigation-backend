// ============================================
// 🔥 CROSS-EXAMINATION ENGINE
// ============================================

export const generateCrossExamination = (
  facts: string,
  analysis: any
) => {
  const questions: string[] = [];

  const lower = (facts || "").toLowerCase();

  // 🔥 Generic Questions
  questions.push("State your name and role in the matter.");
  questions.push("Do you have personal knowledge of the facts stated?");
  questions.push("Is it correct that your statement is based on official records?");

  // 🔥 Issue-based questioning
  if (lower.includes("appointment")) {
    questions.push("Who approved the appointment in question?");
    questions.push("Was the statutory procedure followed?");
    questions.push("Can you produce the selection records?");
  }

  if (lower.includes("termination")) {
    questions.push("Was any notice issued before termination?");
    questions.push("Was the petitioner given an opportunity to be heard?");
  }

  if (lower.includes("delay")) {
    questions.push("What caused the delay in taking action?");
    questions.push("Was the delay intentional or unavoidable?");
  }

  // 🔥 Default
  if (questions.length < 5) {
    questions.push("Is it correct that the authority acted arbitrarily?");
    questions.push("Can you justify the decision under law?");
  }

  return questions;
};
