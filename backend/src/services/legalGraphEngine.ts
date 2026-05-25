import Judgment from "../models/judgment.model";

/**
 * 🧠 LEGAL GRAPH ENGINE (STABLE + TYPESAFE)
 */
export const getRelatedJudgments = async (base: any) => {
  try {
    // =========================================
    // 🔥 Ensure SINGLE document
    // =========================================
    const baseDoc: any = Array.isArray(base) ? base[0] : base;

    if (!baseDoc) {
      return [];
    }

    // =========================================
    // 🔥 Safe field extraction
    // =========================================
    const sections: string[] = baseDoc.sections || [];
    const pointsOfLaw: string[] = baseDoc.pointsOfLaw || [];

    // =========================================
    // 🔥 Build query conditions
    // =========================================
    const conditions: any[] = [];

    if (sections.length > 0) {
      conditions.push({ sections: { $in: sections } });
    }

    if (pointsOfLaw.length > 0) {
      conditions.push({ pointsOfLaw: { $in: pointsOfLaw } });
    }

    if (conditions.length === 0) {
      return [];
    }

    // =========================================
    // 🔥 Fetch related judgments
    // =========================================
    const related = await Judgment.find({
      _id: { $ne: baseDoc._id },
      $or: conditions,
    })
      .select("_id caseNumber pointsOfLaw headnote")
      .limit(20);

    // =========================================
    // 🔥 Ranking (simple relevance)
    // =========================================
    const scored = related.map((doc: any) => {
      let score = 0;

      const text = `${doc.pointsOfLaw?.join(" ")} ${doc.headnote}`.toLowerCase();

      for (const p of pointsOfLaw) {
        if (text.includes(p.toLowerCase())) score += 2;
      }

      for (const s of sections) {
        if (text.includes(s.toLowerCase())) score += 1;
      }

      return {
        ...doc.toObject(),
        score,
      };
    });

    // =========================================
    // 🔥 Sort by relevance
    // =========================================
    scored.sort((a, b) => b.score - a.score);

    return scored;

  } catch (err) {
    console.error("❌ Legal Graph Engine Error:", err);
    return [];
  }
};
