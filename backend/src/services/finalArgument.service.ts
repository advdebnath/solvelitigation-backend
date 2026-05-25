export const generateFinalArguments = (analysis: any, caseLaws: any[]) => {
  const citations = (caseLaws || [])
    .map((c: any) => c.caseNumber || c.id || "Case")
    .join(", ");

  return `
FINAL ORAL ARGUMENTS

1. The present matter raises the following issue:
   ${analysis.issues[0]}

2. It is submitted that the impugned action is arbitrary and violative of settled principles of law.

3. The Hon’ble Court has consistently held in ${citations || "relevant precedents"} that statutory compliance and natural justice are mandatory.

4. Applying the above principles, the respondent authority has acted beyond jurisdiction and in violation of procedural safeguards.

5. Therefore, the petitioner is entitled to relief as prayed.

Respectfully submitted.
`.trim();
};
