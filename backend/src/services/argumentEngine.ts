import { findPrecedents } from "./precedentEngine";

// ============================================
// 🔥 TYPES
// ============================================

type Citation = {
  id: any;
  display: string;
};

// ============================================
// 🔥 ARGUMENT ENGINE (FINAL UPGRADE – QUERY AWARE)
// ============================================

export const generateArgument = async (
  judgment: any,
  query: string = ""
) => {
  try {
    const { headnotes = [], pointOfLaw = [], fullText = "" } = judgment;

    const text = (fullText || "").toLowerCase();
    const q = (query || "").toLowerCase();

    let issue = "";
    let rule: string[] = [];
    let application: string[] = [];
    let conclusion: string[] = [];
    let citations: Citation[] = [];

    // ============================================
    // 🔥 HEADNOTES (PRIMARY)
    // ============================================

    headnotes.forEach((h: any) => {
      if (h.issue && !issue) issue = h.issue;
      if (h.rule) rule.push(h.rule);
      if (h.application) application.push(h.application);
      if (h.conclusion) conclusion.push(h.conclusion);
    });

    // ============================================
    // 🔥 ISSUE (QUERY-AWARE FIX)
    // ============================================

    if (!issue) {
      if (q.includes("murder") || q.includes("302")) {
        issue =
          "Whether conviction under Section 302 IPC is sustainable based on evidence?";
      } else if (text.includes("murder")) {
        issue =
          "Whether conviction for murder is legally sustainable based on evidence?";
      } else if (pointOfLaw.length) {
        issue = `Whether ${pointOfLaw.join(", ")} is established?`;
      } else {
        issue =
          "Whether the prosecution has proved its case beyond reasonable doubt?";
      }
    }

    // ============================================
    // 🔥 RULE ENGINE (QUERY + TEXT BASED)
    // ============================================

    if (q.includes("murder")) {
      rule.push(
        "For conviction under Section 302 IPC, prosecution must prove intention and causation of death"
      );
    }

    if (text.includes("circumstantial")) {
      rule.push(
        "Circumstantial evidence must form a complete chain leading to guilt"
      );
    }

    if (text.includes("chain")) {
      rule.push(
        "All circumstances must be fully established and consistent only with guilt"
      );
    }

    if (text.includes("benefit of doubt")) {
      rule.push("Benefit of doubt must go to accused");
    }

    if (text.includes("beyond reasonable doubt")) {
      rule.push("Prosecution must prove case beyond reasonable doubt");
    }

    if (text.includes("last seen")) {
      rule.push(
        "Last seen theory must be supported by strong corroborative evidence"
      );
    }

    if (text.includes("sole witness")) {
      rule.push("Conviction can be based on reliable sole witness");
    }

    if (text.includes("burden of proof")) {
      rule.push("Burden of proof lies on prosecution");
    }

    // fallback rule
    if (!rule.length) {
      rule.push("Prosecution must prove case beyond reasonable doubt");
    }

    // ============================================
    // 🔥 APPLICATION (REAL EXTRACTION)
    // ============================================

    const sentences = text.split(".").map((s: string) => s.trim());

    sentences.forEach((s: string) => {
      if (
        s.includes("no evidence") ||
        s.includes("not proved") ||
        s.includes("failed to prove") ||
        s.includes("contradiction") ||
        s.includes("inconsistent") ||
        s.includes("not established")
      ) {
        if (s.length > 40) {
          application.push(s);
        }
      }
    });

    if (!application.length) {
      const keyLine = sentences.find(
        (s: string) =>
          s.includes("no evidence") ||
          s.includes("not proved") ||
          s.includes("failed")
      );

      application.push(
        keyLine || "Prosecution evidence is insufficient to establish guilt"
      );
    }

    // ============================================
    // 🔥 CONCLUSION (FIXED LOGIC)
    // ============================================

    const hasAcquittal =
      text.includes("acquitted") ||
      text.includes("set aside") ||
      text.includes("benefit of doubt");

    const hasConviction =
      text.includes("convicted") ||
      text.includes("conviction upheld");

    if (hasAcquittal && !hasConviction) {
      conclusion = ["Accused acquitted"];
    } else if (!hasAcquittal && hasConviction) {
      conclusion = ["Conviction upheld"];
    } else {
      conclusion = ["Benefit of doubt must go to accused"];
    }

    // ============================================
    // 🔥 PRECEDENTS
    // ============================================

    const precedents = await findPrecedents(judgment);

    citations = [
      ...(precedents.supporting || []),
      ...(precedents.similar || []),
    ].slice(0, 5);

    // fallback citation
    if (!citations.length && judgment.caseNumber) {
      citations.push({
        id: judgment._id || "self",
        display: judgment.slscCitation
          ? `${judgment.slscCitation} (${judgment.caseNumber})`
          : judgment.caseNumber,
      });
    }

    // ============================================
    // 🔥 FINAL OUTPUT
    // ============================================

    return {
      issue,
      rule: [...new Set(rule)],
      application: [...new Set(application)],
      conclusion,
      citations,
    };
  } catch (err) {
    console.error("Argument Engine Error:", err);

    return {
      issue: "Unable to generate issue",
      rule: [],
      application: [],
      conclusion: [],
      citations: [],
    };
  }
};
