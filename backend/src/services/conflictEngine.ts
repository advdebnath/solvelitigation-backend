import { getCourtWeight } from "./precedentEngine";

// ============================================
// 🔥 DECISION EXTRACTION (IMPROVED)
// ============================================

const extractDecision = (text: string = "") => {
  const t = text.toLowerCase();

  if (t.includes("appeal allowed") || t.includes("petition allowed")) return "allowed";
  if (t.includes("appeal dismissed") || t.includes("petition dismissed")) return "dismissed";
  if (t.includes("convicted")) return "convicted";
  if (t.includes("acquitted")) return "acquitted";
  if (t.includes("bail granted")) return "bail_granted";
  if (t.includes("bail rejected")) return "bail_rejected";

  return "unknown";
};

// ============================================
// 🔥 CONFLICT DETECTION
// ============================================

export const detectConflicts = (cases: any[]) => {
  const conflicts: any[] = [];

  for (let i = 0; i < cases.length; i++) {
    for (let j = i + 1; j < cases.length; j++) {
      const a = cases[i];
      const b = cases[j];

      const decisionA = extractDecision(a.fullText || "");
      const decisionB = extractDecision(b.fullText || "");

      if (
        decisionA !== "unknown" &&
        decisionB !== "unknown" &&
        decisionA !== decisionB
      ) {
        conflicts.push({
          caseA: a.caseNumber,
          caseB: b.caseNumber,
          conflict: `${decisionA} vs ${decisionB}`,
        });
      }
    }
  }

  return conflicts;
};

// ============================================
// 🔥 OVERRULING DETECTION (SMART)
// ============================================

export const detectOverruling = (cases: any[]) => {
  const overruling: any[] = [];

  for (let i = 0; i < cases.length; i++) {
    const a = cases[i];
    const textA = (a.fullText || "").toLowerCase();

    // 🔥 explicit overruling keywords
    if (
      textA.includes("overruled") ||
      textA.includes("set aside") ||
      textA.includes("reversed")
    ) {
      overruling.push({
        case: a.caseNumber,
        reason: "Explicit overruling language",
      });
      continue;
    }

    // 🔥 fallback: hierarchy-based (controlled)
    for (let j = 0; j < cases.length; j++) {
      if (i === j) continue;

      const b = cases[j];

      const weightA = getCourtWeight(a.caseNumber);
      const weightB = getCourtWeight(b.caseNumber);

      if (weightA > weightB + 2) {
        overruling.push({
          stronger: a.caseNumber,
          weaker: b.caseNumber,
          reason: "Higher court authority",
        });
      }
    }
  }

  return overruling;
};

// ============================================
// 🔥 DISTINGUISHING DETECTION
// ============================================

export const detectDistinguishing = (cases: any[]) => {
  return cases.filter((c) => {
    const t = (c.fullText || "").toLowerCase();

    return (
      t.includes("distinguished") ||
      t.includes("different facts") ||
      t.includes("not applicable")
    );
  });
};

// ============================================
// 🔥 SUPPORTING DETECTION
// ============================================

export const detectSupporting = (cases: any[]) => {
  return cases.filter((c) => {
    const t = (c.fullText || "").toLowerCase();

    return (
      t.includes("relied on") ||
      t.includes("followed") ||
      t.includes("applied")
    );
  });
};

// ============================================
// 🔥 MASTER ENGINE (NORMALIZED)
// ============================================

export const conflictAnalysis = (cases: any[]) => {
  try {
    return {
      conflicts: detectConflicts(cases),
      overruling: detectOverruling(cases),
      distinguishing: detectDistinguishing(cases),
      supporting: detectSupporting(cases),
    };
  } catch (err) {
    console.error("Conflict Engine Error:", err);

    return {
      conflicts: [],
      overruling: [],
      distinguishing: [],
      supporting: [],
    };
  }
};
