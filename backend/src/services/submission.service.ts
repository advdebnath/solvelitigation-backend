export const generateWrittenSubmissions = (
  ctx: any,
  analysis: any,
  caseLaws: any[]
) => {
  const citations = (caseLaws || [])
    .map((c: any) => c.caseNumber || c.id || "Case")
    .join(", ");

  return `
IN THE ${ctx.court}

WRITTEN SUBMISSIONS ON BEHALF OF THE PETITIONER

----------------------------------------

1. INTRODUCTION

The present petition challenges the legality of the impugned action.

----------------------------------------

2. FACTS

${ctx.facts}

----------------------------------------

3. ISSUES

${analysis.issues.map((i: string, idx: number) => `${idx + 1}. ${i}`).join("\n")}

----------------------------------------

4. SUBMISSIONS

4.1 The impugned action is arbitrary and violative of principles of natural justice.

4.2 The authority acted beyond jurisdiction.

4.3 The action is contrary to statutory provisions.

----------------------------------------

5. AUTHORITIES

The petitioner relies upon:
${citations || "Relevant judicial precedents"}

----------------------------------------

6. PRAYER

It is respectfully prayed that this Hon’ble Court may be pleased to allow the petition.

Filed by:
${ctx.petitioner}
`.trim();
};
