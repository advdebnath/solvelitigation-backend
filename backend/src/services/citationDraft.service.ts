// ============================================
// 🔥 CITATION DRAFTING ENGINE
// ============================================

export const generateCitations = (caseLaws: any[]) => {
  if (!caseLaws || caseLaws.length === 0) {
    return "No citations available.";
  }

  return caseLaws
    .map((c, idx) => {
      const name = c.caseNumber || c.id || "Case";
      return `${idx + 1}. ${name} – relied upon for establishing legal principles.`;
    })
    .join("\n");
};
