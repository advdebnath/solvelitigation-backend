export const generateLegalAnswer = (judgments: any[], query: string) => {
  if (!judgments.length) {
    return { message: "No relevant judgments found" };
  }

  const issue = `Whether ${query}?`;

  const rule = [
    "Circumstantial evidence must form a complete chain",
    "Benefit of doubt must go to accused",
  ];

  const analysis = judgments.slice(0, 5).map((j) => {
    const snippet = j.fullText?.slice(0, 200) || "";
    return `${j.caseNumber}: ${snippet}`;
  });

  const conclusion = judgments.slice(0, 3).map((j) => {
    return `${j.caseNumber}: Decision based on evidence`;
  });

  return { issue, rule, analysis, conclusion };
};
