// ============================================
// 🔥 CLAUSE SUGGESTION ENGINE (CLEAN FIXED)
// ============================================

export const suggestClauses = (facts: string) => {
  const lower = (facts || "").toLowerCase();

  const clauses: string[] = [];

  if (lower.includes("natural justice") || lower.includes("no hearing")) {
    clauses.push(
      "Violation of principles of natural justice, particularly audi alteram partem."
    );
  }

  if (lower.includes("jurisdiction")) {
    clauses.push(
      "The authority has acted beyond its jurisdiction and powers conferred by statute."
    );
  }

  if (lower.includes("appointment")) {
    clauses.push(
      "The appointment is contrary to statutory provisions governing the selection process."
    );
  }

  if (lower.includes("delay")) {
    clauses.push(
      "The delay deserves to be condoned in the interest of justice."
    );
  }

  if (clauses.length === 0) {
    clauses.push(
      "The impugned action is arbitrary, illegal and liable to be set aside."
    );
  }

  return clauses;
};
