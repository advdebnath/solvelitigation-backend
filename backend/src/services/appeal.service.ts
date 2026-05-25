// ============================================
// 🔥 APPEAL DRAFTING ENGINE
// ============================================

export const generateAppealDraft = (
  ctx: any,
  analysis: any,
  lowerCourtDecision: string
) => {
  const issues = analysis?.issues || [];

  return `
IN THE ${ctx.court}

${ctx.petitioner} ... Appellant
Versus
${ctx.respondent} ... Respondent

APPEAL

----------------------------------------

IMPUGNED ORDER:

${lowerCourtDecision || "Details of impugned judgment"}

----------------------------------------

FACTS:

${ctx.facts}

----------------------------------------

GROUNDS OF APPEAL:

${issues.map((i: string, idx: number) => `${idx + 1}. ${i}`).join("\n")}

A. The impugned judgment is contrary to law.

B. The findings are arbitrary and unsustainable.

C. The lower court failed to appreciate evidence.

----------------------------------------

PRAYER:

It is most respectfully prayed that this Hon’ble Court may be pleased to:

1. Set aside the impugned judgment.
2. Grant appropriate relief in favour of the appellant.

AND FOR THIS ACT OF KINDNESS, THE APPELLANT SHALL EVER PRAY.

Filed by:
${ctx.petitioner}
`.trim();
};
