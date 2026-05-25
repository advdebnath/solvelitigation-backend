export const generateLegalAnalysis = (facts: string) => {
  if (!facts || facts.trim().length === 0) {
    return {
      issues: [],
      grounds: "",
      arguments: "",
      counterArguments: "",
      prediction: {
        winProbability: 50,
        outcome: "Insufficient data",
      },
    };
  }

  const lower = facts.toLowerCase();

  const issues: string[] = [];

  // ============================================
  // 🔥 ISSUE DETECTION
  // ============================================

  if (lower.includes("appointment")) {
    issues.push("Whether the appointment is valid under law");
  }

  if (lower.includes("termination")) {
    issues.push("Whether the termination is lawful");
  }

  if (lower.includes("delay")) {
    issues.push("Whether delay deserves condonation");
  }

  if (issues.length === 0) {
    issues.push("Whether the impugned action is legally sustainable");
  }

  // ============================================
  // 🔥 GROUNDS
  // ============================================

  const grounds = `
A. Because the impugned action is arbitrary and violative of principles of natural justice.

B. Because the authority acted beyond its jurisdiction.

C. Because the action is contrary to statutory provisions.
`.trim();

  // ============================================
  // 🔥 MAIN ARGUMENT (IMPROVED IRAC)
  // ============================================

  const legalArguments = `
ISSUE:
${issues[0]}

RULE:
It is a settled principle of law that administrative actions must comply with statutory provisions and adhere to the principles of natural justice.

APPLICATION:
From the facts presented, it appears that the authority has exercised its power in a manner inconsistent with the governing statutory framework and without adherence to procedural fairness.

CONCLUSION:
Therefore, the impugned action is legally unsustainable and liable to be set aside by this Hon’ble Court.
`.trim();

  // ============================================
  // 🔥 COUNTER ARGUMENT
  // ============================================

  const counterArguments = `
It may be contended by the respondent that the authority acted within its lawful powers and in accordance with the applicable statutory provisions.

It may further be argued that procedural requirements were substantially complied with and no prejudice has been caused.

Therefore, the impugned action deserves to be upheld.
`.trim();

  // ============================================
  // 🔥 JUDGE PREDICTION (HEURISTIC MODEL)
  // ============================================

  let winProbability = 50;

  // positive signals
  if (lower.includes("violation")) winProbability += 20;
  if (lower.includes("illegal")) winProbability += 15;
  if (lower.includes("no notice")) winProbability += 15;
  if (lower.includes("natural justice")) winProbability += 10;

  // negative signals
  if (lower.includes("delay")) winProbability -= 10;
  if (lower.includes("discretion")) winProbability -= 10;

  // clamp
  if (winProbability > 90) winProbability = 90;
  if (winProbability < 10) winProbability = 10;

  const prediction = {
    winProbability,
    outcome:
      winProbability > 60
        ? "Likely in favour of petitioner"
        : winProbability < 40
        ? "Risky case"
        : "Balanced case",
  };

  // ============================================
  // 🔥 FINAL RETURN
  // ============================================

  return {
    issues,
    grounds,
    arguments: legalArguments,
    counterArguments,
    prediction,
  };
};
