import { buildLegalReport } from "./reportEngine";

// ============================================
// 🏛️ COURT HEADER
// ============================================

const courtHeader = (court: string = "high") => {
  if (court === "supreme") {
    return `
IN THE SUPREME COURT OF INDIA
(CIVIL/CRIMINAL ORIGINAL JURISDICTION)
`;
  }

  return `
IN THE HIGH COURT OF __________
(CIVIL/CRIMINAL JURISDICTION)
`;
};

// ============================================
// 📅 LIST OF DATES
// ============================================

const buildListOfDates = (facts: string) => {
  const lines = facts.split(".").filter((l) => l.trim().length > 10);

  return `
LIST OF DATES

${lines
  .slice(0, 5)
  .map((l, i) => `${i + 1}. ${l.trim()}`)
  .join("\n")}
`;
};

// ============================================
// 🧠 SYNOPSIS
// ============================================

const buildSynopsis = (facts: string, report: any) => {
  return `
SYNOPSIS

The present petition arises out of the following facts:

${facts.slice(0, 500)}

The issues involved relate to:

${report.issue || "Legal issues involved"}

It is submitted that:

${report.rule || "Applicable law"}

Hence, the present petition.
`;
};

// ============================================
// ⚖️ QUESTIONS OF LAW
// ============================================

const buildQuestionsOfLaw = (report: any) => {
  const questions: string[] = [];

  if (report.issue) {
    questions.push(`Whether ${report.issue}?`);
  }

  if (report.rule) {
    questions.push(`Whether the Hon’ble Court erred in applying ${report.rule}?`);
  }

  if (!questions.length) {
    questions.push("Whether the impugned judgment is legally sustainable?");
  }

  return `
QUESTIONS OF LAW

${questions.map((q, i) => `${i + 1}. ${q}`).join("\n")}
`;
};

// ============================================
// 🧠 GROUNDS
// ============================================

const buildGrounds = (report: any) => {
  return `
GROUNDS

A. Because the impugned judgment is contrary to law.
B. Because ${report.rule || "settled legal principles"} have been ignored.
C. Because ${report.application || "facts have been misapplied"}.
D. Because the findings are perverse and unsustainable.
`;
};

// ============================================
// 🧾 COMMON FORMATTERS
// ============================================

const header = (title: string) => `
${title}
`;

const parties = (petitioner = "Petitioner", respondent = "Respondent") => `
Between:

${petitioner}
...Petitioner

Versus

${respondent}
...Respondent
`;

const prayerBlock = () => `
PRAYER

It is most respectfully prayed that this Hon’ble Court may be pleased to:
(a) Grant appropriate relief; and
(b) Pass any other order deemed fit in the interest of justice.
`;

// ============================================
// 📎 ANNEXURE ENGINE
// ============================================

const injectAnnexureRefs = (facts: string, annexures: string[] = []) => {
  if (!annexures.length) return facts;

  let result = facts;

  annexures.slice(0, 2).forEach((a, i) => {
    result += `\nAnnexure A${i + 1}: ${a}`;
  });

  return result;
};

// ============================================
// 🏛️ SLP BUILDER
// ============================================

const buildSLP = (
  facts: string,
  report: any,
  annexures: string[]
) => {
  const updatedFacts = injectAnnexureRefs(facts, annexures);

  return `
${courtHeader("supreme")}

SPECIAL LEAVE PETITION

${buildListOfDates(facts)}

${buildSynopsis(facts, report)}

${buildQuestionsOfLaw(report)}

${buildGrounds(report)}

${parties("Petitioner", "Respondent")}

FACTS
${updatedFacts}

${prayerBlock()}
`;
};

// ============================================
// ⚖️ OTHER PETITIONS
// ============================================

const buildGeneric = (
  title: string,
  facts: string,
  report: any,
  court: string,
  annexures: string[]
) => {
  const updatedFacts = injectAnnexureRefs(facts, annexures);

  return `
${courtHeader(court)}

${buildListOfDates(facts)}

${buildSynopsis(facts, report)}

${header(title)}

${parties()}

FACTS
${updatedFacts}

${buildGrounds(report)}

${prayerBlock()}
`;
};

// ============================================
// 🧠 MAIN ENGINE (FINAL)
// ============================================

export const generatePetition = async ({
  type,
  facts,
  query,
  court = "high",
  annexures = [],
}: {
  type: string;
  facts: string;
  query: string;
  court?: string;
  annexures?: string[];
}) => {
  try {
    const report = await buildLegalReport(query);

    if ((report as any).error) {
      return { error: "No legal data available" };
    }

    if (type === "slp") return buildSLP(facts, report, annexures);

    if (type === "bail") return buildGeneric("BAIL APPLICATION", facts, report, court, annexures);
    if (type === "writ") return buildGeneric("WRIT PETITION", facts, report, court, annexures);

    return buildGeneric("CIVIL SUIT", facts, report, court, annexures);

  } catch (err) {
    console.error("Petition Engine Error:", err);
    return { error: "Petition generation failed" };
  }
};

// ============================================
// 📜 AFFIDAVIT
// ============================================

export const generateAffidavit = (name: string, facts: string) => `
AFFIDAVIT

I, ${name}, do hereby solemnly affirm:

1. That I am the deponent.
2. That the facts stated are true.

${facts}

DEPONENT
`;

// ============================================
// 🖋️ VAKALATNAMA
// ============================================

export const generateVakalatnama = (client: string, advocate: string) => `
VAKALATNAMA

I, ${client}, appoint ${advocate} as Advocate.

Signed:
${client}

Accepted:
${advocate}
`;
