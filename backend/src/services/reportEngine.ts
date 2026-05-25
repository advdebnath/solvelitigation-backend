import axios from "axios";
import Judgment from "../models/judgment.model";
import { generateArgument } from "./argumentEngine";
import { multiCaseReasoning } from "./reasoningEngine";
import { rankPrecedents } from "./precedentEngine";

// ============================================
// 📘 BUILD LEGAL REPORT
// ============================================

export const buildLegalReport = async (query: string) => {
  let cases: any[] = [];

  // 🔥 NLP SEARCH
  try {
    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/semantic/search",
      { query }
    );
    cases = data?.results || [];
  } catch {
    console.warn("⚠️ NLP fallback");
  }

  // 🔥 DB FALLBACK
  if (!cases.length) {
    cases = await Judgment.find({
      $text: { $search: query },
    })
      .select("caseNumber slscCitation fullText headnote pointsOfLaw")
      .limit(10)
      .lean();
  }

  if (!cases.length) {
    return { error: "No cases found" };
  }

  // 🔥 RANK
  cases = rankPrecedents(cases);

  const primary = cases[0];

  // 🔥 ARGUMENT
  const argument = await generateArgument(primary, query);

  // 🔥 REASONING
  const reasoning = await multiCaseReasoning(cases, query);

  // 🔥 CITATIONS
  const citations = cases.map((c: any) => ({
    case: c.caseNumber,
    citation: c.slscCitation || "N/A",
    score: c.precedentScore || 0,
  }));

  return {
    query,
    issue: argument.issue,
    rule: argument.rule,
    application: argument.application,
    conclusion: argument.conclusion,
    reasoning,
    citations,
  };
};
