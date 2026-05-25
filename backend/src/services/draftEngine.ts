export const generateCourtDraft = (argument: any) => {
  try {
    const {
      issue = "",
      rule = [],
      application = [],
      conclusion = [],
      citations = [],
    } = argument;

    // ============================================
    // 🔥 BUILD DRAFT
    // ============================================

    let draft = "";

    draft += `IN THE HON'BLE COURT\n\n`;
    draft += `WRITTEN SUBMISSIONS ON BEHALF OF THE APPLICANT\n\n`;

    // ISSUE
    draft += `1. ISSUE\n`;
    draft += `${issue}\n\n`;

    // RULE
    draft += `2. LEGAL POSITION\n`;
    rule.forEach((r: string) => {
      draft += `- ${r}\n`;
    });
    draft += `\n`;

    // APPLICATION
    draft += `3. APPLICATION TO PRESENT CASE\n`;
    application.forEach((a: string) => {
      draft += `- ${a}\n`;
    });
    draft += `\n`;

    // CONCLUSION
    draft += `4. CONCLUSION\n`;
    conclusion.forEach((c: string) => {
      draft += `- ${c}\n`;
    });
    draft += `\n`;

    // CITATIONS
    draft += `5. RELIANCE ON PRECEDENTS\n`;
    citations.forEach((c: any) => {
      draft += `- ${c.display}\n`;
    });

    return draft;
  } catch (err) {
    console.error("Draft Engine Error:", err);
    return "Draft generation failed.";
  }
};
