import CaseContext from "../models/caseContext.model";

// ============================================
// 🔥 SAFE VALUE HELPER
// ============================================

const safe = (v: any, fallback = "") =>
  v && String(v).trim() ? v : fallback;


// ============================================
// 🔥 CAUSE TITLE
// ============================================

export const generateCauseTitle = (ctx: any) => {
  return `
IN THE ${safe(ctx.court, "COURT").toUpperCase()}

${safe(ctx.petitioner, "Petitioner")} ... Petitioner
Versus
${safe(ctx.respondent, "Respondent")} ... Respondent
`.trim();
};


// ============================================
// 🔥 FULL PETITION (COURT FORMAT)
// ============================================

export const generatePetition = (ctx: any) => {
  return `
${generateCauseTitle(ctx)}

WRIT PETITION

SYNOPSIS:
${safe(ctx.facts, "Facts not provided")}

----------------------------------------

FACTS:

1. ${safe(ctx.facts)}

----------------------------------------

GROUNDS:

A. ${safe(ctx.grounds, "Grounds not specified")}

----------------------------------------

PRAYER:

In view of the above, it is most respectfully prayed that this Hon’ble Court may be pleased to:

${safe(ctx.prayer, "Grant appropriate relief")}

AND FOR THIS ACT OF KINDNESS, THE PETITIONER SHALL EVER PRAY.

Filed by:
${safe(ctx.petitioner)}
`.trim();
};


// ============================================
// 🔥 STAY APPLICATION (LINKED TO PETITION)
// ============================================

export const generateStay = (ctx: any) => {
  return `
${generateCauseTitle(ctx)}

APPLICATION FOR INTERIM STAY

1. That the petitioner has filed the accompanying petition.

2. That the petitioner submits that unless interim relief is granted, irreparable loss will be caused.

3. That the balance of convenience lies in favour of the petitioner.

----------------------------------------

PRAYER:

It is therefore prayed that this Hon’ble Court may kindly stay the operation of the impugned action.

Filed by:
${safe(ctx.petitioner)}
`.trim();
};


// ============================================
// 🔥 DELAY CONDONATION (DETAILED)
// ============================================

export const generateDelay = (ctx: any) => {
  return `
${generateCauseTitle(ctx)}

APPLICATION FOR CONDONATION OF DELAY

1. That the petitioner submits that the delay in filing the petition occurred due to bona fide reasons.

2. That the delay is neither intentional nor deliberate.

3. That substantial justice would be defeated if delay is not condoned.

----------------------------------------

PRAYER:

It is therefore prayed that this Hon’ble Court may kindly condone the delay in filing the petition.

Filed by:
${safe(ctx.petitioner)}
`.trim();
};


// ============================================
// 🔥 NOTICE (FORMAL)
// ============================================

export const generateNotice = (ctx: any) => {
  return `
${generateCauseTitle(ctx)}

NOTICE

To,
${safe(ctx.respondent)}

Whereas the above petition has been filed by the petitioner,  
you are hereby directed to appear before this Hon’ble Court  
on the date fixed and show cause.

Take notice accordingly.

Dated: ______
`.trim();
};


// ============================================
// 🔥 AFFIDAVIT (NEW)
// ============================================

export const generateAffidavit = (ctx: any) => {
  return `
${generateCauseTitle(ctx)}

AFFIDAVIT

I, ${safe(ctx.petitioner)}, do hereby solemnly affirm and state:

1. That I am the petitioner in the present case.

2. That the contents of the accompanying petition are true to my knowledge and belief.

Verified at ______ on this ___ day of ______.

Deponent:
${safe(ctx.petitioner)}
`.trim();
};


// ============================================
// 🔥 FULL BUNDLE (FINAL)
// ============================================

export const generateBundle = async (caseId: string) => {
  const ctx = await CaseContext.findOne({ caseId });

  if (!ctx) {
    throw new Error("Case context not found");
  }

  return {
    petition: generatePetition(ctx),
    stay: generateStay(ctx),
    delay: generateDelay(ctx),
    notice: generateNotice(ctx),
    affidavit: generateAffidavit(ctx)
  };
};
