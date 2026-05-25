// ============================================
// 🔥 LEGAL PROCESSOR (FINAL PRODUCTION VERSION)
// ============================================

// ============================================
// ✅ CLEAN TEXT
// ============================================

export const cleanText = (text: string = ""): string => {
  return text
    .replace(/\n/g, " ")
    .replace(/signature not verified/gi, "")
    .replace(/digitally signed.*?\d{4}/gi, "")
    .replace(/reportable|non[-\s]?reportable/gi, "")
    .replace(/in the supreme court of india/gi, "")
    .replace(/\s+/g, " ")
    .trim();
};

// ============================================
// ✅ CATEGORY DETECTION
// ============================================

export const detectCategory = (text: string): string => {
  const t = text.toLowerCase();

  if (t.includes("ipc") || t.includes("criminal")) return "Criminal";
  if (t.includes("plaintiff") || t.includes("defendant") || t.includes("suit"))
    return "Civil";
  if (t.includes("dismissal") || t.includes("departmental"))
    return "Service";
  if (t.includes("tax") || t.includes("gst") || t.includes("assessment"))
    return "Taxation";

  return "Unknown";
};

// ============================================
// ✅ LEGAL POINT EXTRACTION (HYBRID ENGINE)
// ============================================

export const extractLegalPoints = (text: string): string[] => {
  const t = text.toLowerCase();
  const points = new Set<string>();

  const category = detectCategory(t);

  // 🔴 CRIMINAL
  if (category === "Criminal") {
    if (t.includes("section 302")) points.add("Murder");
    if (t.includes("section 307")) points.add("Attempt to Murder");
    if (t.includes("evidence")) points.add("Evidence");
    if (t.includes("circumstantial")) points.add("Circumstantial Evidence");
    if (t.includes("benefit of doubt")) points.add("Benefit of Doubt");
    if (t.includes("section 482")) points.add("Quashing of Proceedings");
  }

  // 🔵 CIVIL
  if (category === "Civil") {
    if (t.includes("contract")) points.add("Breach of Contract");
    if (t.includes("agreement")) points.add("Contract Interpretation");
    if (t.includes("specific performance")) points.add("Specific Performance");
    if (t.includes("injunction")) points.add("Injunction");
    if (t.includes("property")) points.add("Property Dispute");
  }

  // 🟡 SERVICE
  if (category === "Service") {
    if (t.includes("dismissal")) points.add("Dismissal from Service");
    if (t.includes("reinstatement")) points.add("Reinstatement");
    if (t.includes("departmental")) points.add("Departmental Proceedings");
  }

  // 🟢 TAX
  if (category === "Taxation") {
    if (t.includes("gst")) points.add("GST");
    if (t.includes("income tax")) points.add("Income Tax");
    if (t.includes("assessment")) points.add("Tax Assessment");
  }

  // ⚙️ COMMON
  if (t.includes("fraud")) points.add("Fraud");
  if (t.includes("arbitration")) points.add("Arbitration");
  if (t.includes("motor vehicles act")) points.add("Motor Vehicles Act");

  return Array.from(points);
};

// ============================================
// ✅ ACT + SECTION EXTRACTOR (NEW)
// ============================================

export const extractActsAndSections = (text: string) => {
  const acts = new Set<string>();
  const sections = new Set<string>();

  const t = text.toLowerCase();

  if (t.includes("ipc")) acts.add("Indian Penal Code");
  if (t.includes("crpc")) acts.add("Criminal Procedure Code");
  if (t.includes("evidence act")) acts.add("Indian Evidence Act");
  if (t.includes("contract act")) acts.add("Indian Contract Act");

  // 🔥 section detection
  const matches = t.match(/section\s+\d+/g);
  if (matches) {
    matches.forEach((m) => sections.add(m.toUpperCase()));
  }

  return {
    acts: Array.from(acts),
    sections: Array.from(sections),
  };
};

// ============================================
// ✅ PARTY EXTRACTION (IMPROVED)
// ============================================

export const extractParties = (text: string = "") => {
  try {
    const cleaned = cleanText(text);

    const match = cleaned.match(
      /(.+?)\s+versus\s+(.+?)(?=judgment|$)/i
    );

    if (!match) return { petitioner: null, respondent: null };

    return {
      petitioner: match[1].trim().slice(-120),
      respondent: match[2].trim().slice(0, 120),
    };
  } catch {
    return { petitioner: null, respondent: null };
  }
};

// ============================================
// ✅ HEADNOTE GENERATOR (IMPROVED)
// ============================================

export const generateHeadnote = (text: string = "") => {
  const t = text.toLowerCase();

  const parts: string[] = [];

  if (t.includes("contract")) parts.push("Contract");
  if (t.includes("breach")) parts.push("Breach");
  if (t.includes("criminal")) parts.push("Criminal");
  if (t.includes("murder")) parts.push("Murder");
  if (t.includes("circumstantial")) parts.push("Circumstantial Evidence");

  if (parts.length === 0) return "Legal issue decided.";

  return parts.join(" – ") + " – Issue decided.";
};

// ============================================
// ✅ POINTS OF LAW CLEANER (RESTORED)
// ============================================

export const cleanPointsOfLaw = (points: string[] = []) => {
  if (!points || !Array.isArray(points)) return [];

  return Array.from(
    new Set(
      points.map((p) =>
        p
          .toLowerCase()
          .replace(/\s+/g, " ")
          .trim()
      )
    )
  );
};
