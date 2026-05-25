import Judgment from "../models/judgment.model";

// ============================================
// 🔗 CITATION ENGINE
// ============================================

export const getCitations = async (doc: any) => {
  const keywords = (doc.pointsOfLaw || []).slice(0, 5);

  if (!keywords.length) return [];

  const related = await Judgment.find({
    _id: { $ne: doc._id },
    pointsOfLaw: { $in: keywords },
  })
    .select("_id caseNumber headnote")
    .limit(10)
    .lean();

  return related.map((c: any) => ({
    id: c._id,
    caseNumber: c.caseNumber,
    summary: c.headnote,
  }));
};
