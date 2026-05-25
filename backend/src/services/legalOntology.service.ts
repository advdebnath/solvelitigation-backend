// =====================================================
// 🔥 SOLVELITIGATION LEGAL ONTOLOGY ENGINE (UPGRADED)
// =====================================================

export type LegalCategory =
  | "Criminal"
  | "Civil"
  | "Service Law"
  | "Taxation & Corporate"
  | "Unknown";

// =====================================================
// 🔥 CATEGORY NORMALIZATION
// =====================================================

const CATEGORY_NORMALIZATION:
Record<string, LegalCategory> = {

  "criminal": "Criminal",
  "criminal law": "Criminal",
  "crime": "Criminal",

  "civil": "Civil",
  "civil law": "Civil",
  "constitutional": "Civil",

  "service": "Service Law",
  "service law": "Service Law",
  "servicelaw": "Service Law",

  "taxation": "Taxation & Corporate",
  "corporate": "Taxation & Corporate",
  "tax": "Taxation & Corporate",

  "unknown": "Unknown"
};

// =====================================================
// 🔥 NORMALIZE CATEGORY
// =====================================================

export const normalizeCategory = (
  rawCategory: string = ""
): LegalCategory => {

  const cleaned =
    rawCategory
      .trim()
      .toLowerCase();

  return (
    CATEGORY_NORMALIZATION[cleaned]
    || "Unknown"
  );
};

// =====================================================
// 🔥 CATEGORY KEYWORDS
// =====================================================

const CATEGORY_KEYWORDS:
Record<LegalCategory, string[]> = {

  "Criminal": [

    "ipc",
    "bns",
    "bnss",
    "crpc",
    "criminal",
    "crime",
    "murder",
    "rape",
    "dowry",
    "ndps",
    "pocso",
    "bail",
    "fir",
    "chargesheet",
    "investigation",
    "conviction",
    "acquittal",
    "sentence",
    "evidence",
    "cheque bounce",
    "negotiable instruments",
    "pmla",
    "money laundering",
    "prevention of corruption",
    "uapa",
    "terror",
    "narcotic"
  ],

  "Civil": [

    "civil",
    "contract",
    "property",
    "partition",
    "succession",
    "specific relief",
    "transfer of property",
    "injunction",
    "lease",
    "rent",
    "arbitration",
    "family",
    "marriage",
    "consumer",
    "motor vehicle",
    "wakf",
    "title dispute",
    "civil procedure",
    "constitution",
    "article 14",
    "article 21"
  ],

  "Service Law": [

    "service",
    "departmental",
    "disciplinary",
    "promotion",
    "seniority",
    "pension",
    "reinstatement",
    "termination",
    "dismissal",
    "army",
    "navy",
    "air force",
    "civil services",
    "administrative tribunal",
    "departmental inquiry",
    "charge memo",
    "service benefits",
    "conduct rules",
    "ccs",
    "cat"
  ],

  "Taxation & Corporate": [

    "gst",
    "income tax",
    "customs",
    "excise",
    "tax",
    "assessment",
    "reassessment",
    "refund",
    "input tax credit",
    "corporate",
    "companies act",
    "ibc",
    "insolvency",
    "nclt",
    "liquidation",
    "shareholder",
    "board resolution",
    "sebi",
    "fema",
    "rbi",
    "sarfaesi",
    "banking"
  ],

  "Unknown": []
};

// =====================================================
// 🔥 INVALID CROSS-ONTOLOGY TOPICS
// =====================================================

const INVALID_COMBINATIONS = [

  ["murder", "arbitration"],
  ["ndps", "tenancy"],
  ["insolvency", "bail"],
  ["partition", "cheque bounce"],
  ["service", "murder"],
  ["corporate", "rape"]
];

// =====================================================
// 🔥 NORMALIZE ACT NAME
// =====================================================

export const normalizeActName = (
  actName: string = ""
): string => {

  return actName
    .replace(/\s+/g, " ")
    .replace(/[.,]/g, "")
    .trim()
    .toLowerCase();
};

// =====================================================
// 🔥 CASE NUMBER VALIDATOR
// =====================================================

export const isValidCaseNumber = (
  caseNumber: string = ""
): boolean => {

  const text =
    caseNumber.toLowerCase();

  if (
    text.includes("unknown case") ||
    text.includes("item no") ||
    text.includes("notice")
  ) {
    return false;
  }

  return text.length >= 10;
};

// =====================================================
// 🔥 INFER CATEGORY FROM ACT
// =====================================================

export const inferCategoryFromAct = (
  actName: string = ""
): LegalCategory => {

  const normalized =
    normalizeActName(actName);

  let bestCategory:
  LegalCategory = "Unknown";

  let bestScore = 0;

  for (
    const [category, keywords]
    of Object.entries(CATEGORY_KEYWORDS)
  ) {

    let score = 0;

    for (const keyword of keywords) {

      if (
        normalized.includes(
          keyword.toLowerCase()
        )
      ) {
        score++;
      }
    }

    if (score > bestScore) {

      bestScore = score;

      bestCategory =
        category as LegalCategory;
    }
  }

  return bestCategory;
};

// =====================================================
// 🔥 CASE NUMBER CATEGORY
// =====================================================

export const inferCategoryFromCaseNumber = (
  caseNumber: string = ""
): LegalCategory => {

  const text =
    caseNumber.toLowerCase();

  if (
    text.includes("criminal") ||
    text.includes("crl") ||
    text.includes("bail")
  ) {
    return "Criminal";
  }

  if (
    text.includes("service")
  ) {
    return "Service Law";
  }

  if (
    text.includes("tax") ||
    text.includes("gst")
  ) {
    return "Taxation & Corporate";
  }

  if (
    text.includes("civil") ||
    text.includes("writ")
  ) {
    return "Civil";
  }

  return "Unknown";
};

// =====================================================
// 🔥 SECTION FALLBACK
// =====================================================

export const inferCategoryFromSections = (
  sections: any[] = []
): LegalCategory => {

  for (const s of sections) {

    const act =
      String(
        s?.act || ""
      );

    const inferred =
      inferCategoryFromAct(act);

    if (inferred !== "Unknown") {

      return inferred;
    }
  }

  return "Unknown";
};

// =====================================================
// 🔥 FILTER INVALID TOPICS
// =====================================================

export const removeInvalidOntologyTopics = (
  topics: string[] = []
): string[] => {

  const cleaned =
    topics.map(t =>
      t.toLowerCase()
    );

  for (const pair of INVALID_COMBINATIONS) {

    const hasA =
      cleaned.some(t =>
        t.includes(pair[0])
      );

    const hasB =
      cleaned.some(t =>
        t.includes(pair[1])
      );

    if (hasA && hasB) {

      return topics.filter(
        t =>
          !t.toLowerCase().includes(pair[1])
      );
    }
  }

  return topics;
};

// =====================================================
// 🔥 FILTER ACTS BY CATEGORY
// =====================================================

export const filterActsByCategory = (
  acts: string[] = [],
  category: string = ""
): string[] => {

  return acts.filter(act => {

    const inferred =
      inferCategoryFromAct(act);

    return inferred === category;
  });
};

// =====================================================
// 🔥 DOCUMENT QUALITY ENGINE
// =====================================================

export const calculateDocumentQuality = (
  judgment: any
): string => {

  const caseNumber =
    String(
      judgment?.caseNumber || ""
    );

  const headnote =
    String(
      judgment?.headnote || ""
    );

  const acts =
    judgment?.acts || [];

  if (
    !isValidCaseNumber(caseNumber)
  ) {
    return "LOW_QUALITY";
  }

  if (
    headnote.includes("para-unknown")
  ) {
    return "LOW_QUALITY";
  }

  if (
    acts.includes("Unknown Act")
  ) {
    return "LOW_QUALITY";
  }

  return "HIGH_QUALITY";
};

// =====================================================
// 🔥 REVIEW REQUIRED
// =====================================================

export const requiresManualReview = (
  judgment: any
): boolean => {

  if (
    judgment?.category === "Unknown"
  ) {
    return true;
  }

  if (
    judgment?.documentQuality ===
    "LOW_QUALITY"
  ) {
    return true;
  }

  if (
    judgment?.acts?.includes(
      "Unknown Act"
    )
  ) {
    return true;
  }

  return false;
};

// =====================================================
// 🔥 AUTO GROUP ACTS
// =====================================================

export const autoGroupActs = (
  acts: string[] = []
) => {

  const grouped:
  Record<string, string[]> = {};

  for (const act of acts) {

    const category =
      inferCategoryFromAct(act);

    if (!grouped[category]) {

      grouped[category] = [];
    }

    grouped[category].push(act);
  }

  return grouped;
};

// =====================================================
// 🔥 HELPERS
// =====================================================

export const isCriminalAct = (
  act: string
) =>
  inferCategoryFromAct(act)
  === "Criminal";

export const isCivilAct = (
  act: string
) =>
  inferCategoryFromAct(act)
  === "Civil";

export const isServiceLawAct = (
  act: string
) =>
  inferCategoryFromAct(act)
  === "Service Law";

export const isTaxCorporateAct = (
  act: string
) =>
  inferCategoryFromAct(act)
  === "Taxation & Corporate";
