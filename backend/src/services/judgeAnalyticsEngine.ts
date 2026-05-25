import JudgeProfile from "../models/judgeProfile.model";

// ============================================
// 🧠 EXTRACT JUDGES (SIMPLE VERSION)
// ============================================

export const extractJudges = (text: string = "") => {
  const matches = text.match(/Justice\s+[A-Z][a-zA-Z\s]+/g);
  return matches || [];
};

// ============================================
// 📊 UPDATE JUDGE PROFILE
// ============================================

export const updateJudgeProfile = async (
  judgment: any
) => {
  try {
    const judges = extractJudges(judgment.fullText || "");

    for (const j of judges) {
      const name = j.trim();

      let profile = await JudgeProfile.findOne({ name });

      if (!profile) {
        profile = new JudgeProfile({ name });
      }

      profile.totalCases += 1;

      // Simple outcome detection
      const text = (judgment.fullText || "").toLowerCase();

      if (text.includes("allowed")) profile.allowed += 1;
      if (text.includes("dismissed") || text.includes("rejected"))
        profile.rejected += 1;

      if (text.includes("bail granted")) profile.bailGranted += 1;
      if (text.includes("bail rejected")) profile.bailRejected += 1;

      if (text.includes("held") || text.includes("observed"))
        profile.precedentHeavy += 1;

      await profile.save();
    }

  } catch (err) {
    console.error("Judge Profile Update Error:", err);
  }
};

// ============================================
// 📈 BUILD JUDGE PROFILE SUMMARY
// ============================================

export const getJudgeInsights = async (cases: any[]) => {
  try {
    const names = new Set<string>();

    cases.forEach((c) => {
      const j = extractJudges(c.fullText || "");
      j.forEach((n) => names.add(n.trim()));
    });

    const profiles = await JudgeProfile.find({
      name: { $in: Array.from(names) },
    });

    if (!profiles.length) return null;

    // Aggregate
    let total = 0;
    let allowed = 0;
    let rejected = 0;
    let bailGranted = 0;
    let bailRejected = 0;

    profiles.forEach((p) => {
      total += p.totalCases;
      allowed += p.allowed;
      rejected += p.rejected;
      bailGranted += p.bailGranted;
      bailRejected += p.bailRejected;
    });

    const successRate = total ? (allowed / total) * 100 : 0;

    return {
      judges: profiles.map((p) => p.name),
      successRate: Math.round(successRate),
      bailTrend:
        bailGranted > bailRejected ? "Liberal" : "Conservative",
    };

  } catch (err) {
    console.error("Judge Insight Error:", err);
    return null;
  }
};
