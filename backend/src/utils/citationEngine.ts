// ============================================
// 🔥 CITATION ENGINE (PRODUCTION)
// ============================================

export const buildCitations = (cases: any[]) => {
  if (!cases || !cases.length) return [];

  return cases.map((c) => ({
    id: c._id,

    caseNumber: c.caseNumber || "UNKNOWN",

    slscCitation: c.slscCitation || null,

    display: c.slscCitation
      ? `${c.slscCitation} (${c.caseNumber})`
      : c.caseNumber,
  }));
};
