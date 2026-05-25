import { suggestClauses } from "./clause.service";
import { generateCitations } from "./citationDraft.service";

// ============================================
// 🔥 PETITION DRAFTING ENGINE (UPGRADED)
// ============================================

export const generatePetitionDraft = (
  ctx: any,
  analysis: any,
  caseLaws: any[] = []
) => {
  // 🔥 SAFE FALLBACKS
  const petitioner = ctx?.petitioner || "Petitioner";
  const respondent = ctx?.respondent || "Respondent";
  const court = ctx?.court || "COURT";
  const facts = ctx?.facts || "No facts provided";

  const issues =
    analysis?.issues?.length > 0
      ? analysis.issues
      : ["Whether the impugned action is legally sustainable"];

  const grounds = analysis?.grounds || "No grounds available";
  const argumentsText = analysis?.arguments || "No arguments available";

  // 🔥 NEW ENGINES
  const clauses = suggestClauses(facts);
  const citations = generateCitations(caseLaws);

  return `
IN THE ${court}

${petitioner} ... Petitioner
Versus
${respondent} ... Respondent

WRIT PETITION

----------------------------------------

SYNOPSIS:

${facts}

----------------------------------------

FACTS:

1. ${facts}

----------------------------------------

ISSUES:

${issues.map((i: string, idx: number) => `${idx + 1}. ${i}`).join("\n")}

----------------------------------------

GROUNDS:

${grounds}

----------------------------------------

ADDITIONAL LEGAL GROUNDS:

${clauses.map((c, i) => `${i + 1}. ${c}`).join("\n")}

----------------------------------------

ARGUMENTS:

${argumentsText}

----------------------------------------

CITATIONS:

${citations}

----------------------------------------

PRAYER:

In view of the above, it is most respectfully prayed that this Hon’ble Court may be pleased to:

${ctx?.prayer || "Grant appropriate relief as deemed fit."}

AND FOR THIS ACT OF KINDNESS, THE PETITIONER SHALL EVER PRAY.

----------------------------------------

Filed by:
${petitioner}
`.trim();
};
