export const generateStrategy = (analysis: any) => {
  const { issues, prediction } = analysis;

  let strategy = "";
  let risks = "";
  let suggestions = "";

  // ============================================
  // 🔥 STRATEGY
  // ============================================

  strategy = `
Focus on establishing illegality, violation of statutory provisions, and breach of natural justice.

Primary issue:
${issues[0]}
`.trim();

  // ============================================
  // 🔥 RISKS
  // ============================================

  if (prediction.winProbability < 40) {
    risks = "Case is weak. Strong factual and documentary support required.";
  } else if (prediction.winProbability < 60) {
    risks = "Case is balanced. Arguments must be carefully structured.";
  } else {
    risks = "Case is favourable but must still address counter-arguments.";
  }

  // ============================================
  // 🔥 SUGGESTIONS
  // ============================================

  suggestions = `
✔ Emphasize statutory violations  
✔ Highlight procedural lapses  
✔ Counter respondent’s jurisdiction argument  
✔ Support with case laws  
`.trim();

  return {
    strategy,
    risks,
    suggestions,
  };
};
