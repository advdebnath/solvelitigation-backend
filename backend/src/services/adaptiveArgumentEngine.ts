import { unifiedLegalAnalysis } from "./unifiedLegalEngine";
import { generateArgument } from "./argumentEngine";
import * as cheerio from "cheerio";

// ============================================
// 🧠 COURT PRIORITY (SC > HC > Others)
// ============================================

const getCourtPriority = (c: any) => {
  const text = (c?.caseNumber || "").toUpperCase();

  if (text.includes("SUPREME")) return 3;
  if (text.includes("HIGH")) return 2;
  return 1;
};

// ============================================
// 🧠 TEXT RATIO EXTRACTION (FALLBACK)
// ============================================

const extractRatio = (text: string = "") => {
  if (!text) return "";

  const lines = text.split(/[\n\.]/);

  const keywords = [
    "held",
    "it is held",
    "we hold",
    "the court held",
    "observed",
    "ruled",
    "decided",
  ];

  const filtered = lines
    .map((l) => l.trim())
    .filter(
      (l) =>
        l.length > 50 &&
        keywords.some((k) => l.toLowerCase().includes(k))
    )
    .slice(0, 3);

  return filtered.join(". ");
};

// ============================================
// 🧠 HTML RATIO EXTRACTION (PRIMARY)
// ============================================

const extractRatioFromHTML = (html: string = "") => {
  if (!html) return [];

  const $ = cheerio.load(html);

  const results: { text: string; para: number }[] = [];

  $("p, div").each((i, el) => {
    const text = $(el).text().trim();

    if (!text || text.length < 60) return;

    const lower = text.toLowerCase();

    if (
      lower.includes("held") ||
      lower.includes("it is held") ||
      lower.includes("we hold") ||
      lower.includes("observed") ||
      lower.includes("therefore")
    ) {
      results.push({
        text,
        para: i + 1,
      });
    }
  });

  return results.slice(0, 5);
};

// ============================================
// 🎯 CONTEXT FILTER (ISSUE MATCH)
// ============================================

const matchRatioWithIssue = (
  ratioText: string = "",
  query: string = "",
  issue: string = ""
) => {
  if (!ratioText) return "";

  const context = `${query} ${issue}`.toLowerCase();
  const keywords = context.split(/\s+/).filter((w) => w.length > 4);

  const lines = ratioText.split(".").map((l) => l.trim());

  const scored = lines.map((line) => {
    let score = 0;

    keywords.forEach((k) => {
      if (line.toLowerCase().includes(k)) score += 2;
    });

    if (line.toLowerCase().includes("held")) score += 2;
    if (line.toLowerCase().includes("court")) score += 1;

    return { line, score };
  });

  return scored
    .sort((a, b) => b.score - a.score)
    .slice(0, 1)
    .map((s) => s.line)
    .join(". ");
};

// ============================================
// 🔥 RANK CITATIONS (HTML + TEXT HYBRID)
// ============================================

const rankCitations = (citations: any[] = [], query: string = "") => {
  return citations
    .map((c: any) => {
      let ratioText = "";
      let paraRef = "";

      // 🔥 HTML PRIMARY
      if (c?.html) {
        const htmlRatios = extractRatioFromHTML(c.html);

        const filtered = htmlRatios
          .map((r) => ({
            ...r,
            score: matchRatioWithIssue(
              r.text,
              query,
              c?.issue || ""
            ).length,
          }))
          .sort((a, b) => b.score - a.score);

        if (filtered.length) {
          ratioText = filtered[0].text;
          paraRef = `(para-${filtered[0].para})`;
        }
      }

      // 🔁 TEXT FALLBACK
      if (!ratioText) {
        const rawRatio = extractRatio(c?.fullText || "");

        ratioText = matchRatioWithIssue(
          rawRatio,
          query,
          c?.issue || ""
        );
      }

      return {
        ...c,
        ratio: ratioText,
        para: paraRef,
        score:
          getCourtPriority(c) * 10 +
          (c?.pointsOfLaw?.length || 0) * 2 +
          (c?.fullText?.length || 0) / 1000,
      };
    })
    .sort((a, b) => b.score - a.score);
};

// ============================================
// 🔗 BUILD CITATION LINKS (WITH LABELS)
// ============================================

const buildCitationLinks = (citations: any[] = [], query: string = "") => {
  const ranked = rankCitations(citations, query);

  return ranked.map((c: any, i: number) => {
    const id = c?._id || c?.id || "";
    const name = c?.caseNumber || c?.title || "Case Law";

    const label =
      i === 0
        ? "🔥 STRONGEST PRECEDENT"
        : getCourtPriority(c) === 3
        ? "⚖️ SUPREME COURT"
        : "";

    return {
      link: `<a href="/judgment/${id}" target="_blank">${name}</a>`,
      label,
      ratio: c?.ratio || "",
      para: c?.para || "",
    };
  });
};

// ============================================
// 🏛️ DETECT COURT TYPE
// ============================================

const detectCourtType = (cases: any[]) => {
  const text = JSON.stringify(cases || []).toUpperCase();

  if (text.includes("SUPREME")) return "supreme";
  if (text.includes("HIGH COURT") || text.includes("HC")) return "high";
  if (text.includes("TRIBUNAL")) return "tribunal";

  return "general";
};

// ============================================
// ⚖️ COURT DRAFT
// ============================================

const buildCourtDraft = (base: any, strength: string, query: string) => {
  const citations = buildCitationLinks(base?.citations || [], query);

  return `
IN THE HON'BLE COURT OF COMPETENT JURISDICTION

WRITTEN SUBMISSIONS

1. ISSUE

Whether ${base?.issue || "the impugned action is legally sustainable"}.

2. FACTUAL BACKGROUND

${(base?.application || []).map((a: string, i: number) => `${i + 1}. ${a}`).join("\n")}

3. SUBMISSIONS

A. LEGAL POSITION

${(base?.rule || []).map((r: string, i: number) => {
  const c = citations[i];

  const cite = c ? ` (See: ${c.link} ${c.label})` : "";
  const ratio = c?.ratio ? `\n   ➤ ${c.ratio} ${c.para}` : "";

  return `${i + 1}. ${r}${cite}${ratio}`;
}).join("\n")}

B. APPLICATION TO FACTS

${(base?.application || []).map((a: string, i: number) => `${i + 1}. ${a}`).join("\n")}

4. CONCLUSION

${
  strength === "strong"
    ? "Supported by binding precedents."
    : strength === "weak"
    ? "Requires equitable consideration."
    : "Requires judicial determination."
}

5. AUTHORITIES

${citations.map((c: any, i: number) => `${i + 1}. ${c.link}`).join("\n")}

6. PRAYER

Relief may kindly be granted.

`;
};

// ============================================
// 🧠 MAIN ENGINE
// ============================================

export const generateAdaptiveArgument = async (
  cases: any[],
  query: string
) => {
  try {
    if (!cases?.length) {
      return {
        legalStrength: "error",
        argument: "No cases available",
      };
    }

    const analysis = await unifiedLegalAnalysis(cases, query);
    const base = await generateArgument(cases[0], query);

    const score = analysis?.successProbability || 50;

    let strength = "moderate";
    if (score > 70) strength = "strong";
    else if (score < 40) strength = "weak";

    const argument = buildCourtDraft(base, strength, query);

    return {
      successProbability: score,
      legalStrength: strength,
      courtType: detectCourtType(cases),
      argument,
      reasoning: analysis?.reasoning || "",
    };

  } catch (err) {
    console.error("Adaptive Argument Error:", err);

    return {
      legalStrength: "error",
      argument: "Argument generation failed",
    };
  }
};
