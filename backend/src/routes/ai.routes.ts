import { generateAdaptiveArgument } from "../services/adaptiveArgumentEngine";
import express from "express";
import axios from "axios";
import fs from "fs";
import Judgment from "../models/judgment.model";

// 🔥 ENGINES
import { generateArgument } from "../services/argumentEngine";
import { generateCourtDraft } from "../services/draftEngine";
import { explainJudgment } from "../services/explainEngine";
import { getCitations } from "../services/citationEngine";
import {
  multiCaseReasoning,
  judgeSimulation,
} from "../services/reasoningEngine";
import { conflictAnalysis } from "../services/conflictEngine";
import { generateJudgeDecision } from "../services/judgeEngine";
import { unifiedLegalAnalysis } from "../services/unifiedLegalEngine";

// 🔥 REPORT ENGINE
import { buildLegalReport } from "../services/reportEngine";
import { generatePDF } from "../services/pdfEngine";

// 🔥 PETITION ENGINE
import { generatePetition } from "../services/petitionEngine";
import { generatePetitionPDF } from "../services/petitionPdf";

// 🔥 BUNDLE ENGINE
import { generateBundlePDF } from "../services/bundleEngine";

const router = express.Router();

// ============================================
// CASE RANKING
// ============================================

const rankCases = (cases: any[]) => {
  return cases.sort((a, b) => {
    const score = (c: any) => {
      let s = 0;

      if (c.caseNumber?.includes("SUPREME")) s += 5;
      if (c.caseNumber?.includes("APPEAL")) s += 3;
      if (c.caseNumber?.includes("SLP")) s += 1;

      if (c.headnote) s += 2;
      if (c.pointsOfLaw?.length) s += 2;

      return s;
    };

    return score(b) - score(a);
  });
};

// ============================================
// 🔥 AI QUERY
// ============================================

router.post("/ask", async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({ success: false, message: "Query required" });
    }

    let cases: any[] = [];

    try {
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/semantic/search",
        { query },
        { timeout: 8000 }
      );
      cases = data?.results || [];
    } catch {}

    if (!cases.length) {
      cases = await Judgment.find({ $text: { $search: query } }).limit(5);
    }

    if (!cases.length) {
      return res.json({ success: false, message: "No cases found" });
    }

    cases = rankCases(cases);

    const argument = await generateArgument(cases[0], query);

    return res.json({ success: true, ...argument });

  } catch (err) {
    console.error("ASK ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// 🧠 MULTI CASE REASONING
// ============================================

router.post("/reason", async (req, res) => {
  try {
    const { query } = req.body;

    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/semantic/search",
      { query },
      { timeout: 8000 }
    );

    const cases = data?.results || [];

    if (!cases.length) {
      return res.json({ success: false, message: "No cases found" });
    }

    const reasoning = await multiCaseReasoning(cases, query);

    return res.json({ success: true, ...reasoning });

  } catch (err) {
    console.error("REASON ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// ⚖️ JUDGE SIMULATION
// ============================================

router.post("/judge", async (req, res) => {
  try {
    const { query } = req.body;

    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/semantic/search",
      { query },
      { timeout: 8000 }
    );

    const cases = data?.results || [];

    if (!cases.length) {
      return res.json({ success: false, message: "No cases found" });
    }

    const result = await judgeSimulation(cases, query);

    return res.json({ success: true, judgment: result });

  } catch (err) {
    console.error("JUDGE ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// ⚖️ AI JUDGE DECISION
// ============================================

router.post("/judge-ai", async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({
        success: false,
        message: "Query required",
      });
    }

    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/semantic/search",
      { query },
      { timeout: 8000 }
    );

    const cases = data?.results || [];

    if (!cases.length) {
      return res.json({
        success: false,
        message: "No cases found",
      });
    }

    const result = await generateJudgeDecision(cases, query);

    return res.json({
      success: true,
      query,
      ...result,
    });

  } catch (err) {
    console.error("AI JUDGE ERROR:", err);

    return res.status(500).json({
      success: false,
      message: "AI decision failed",
    });
  }
});

// ============================================
// 🧠 UNIFIED LEGAL AI (FINAL CORE)
// ============================================

router.post("/legal-ai", async (req, res) => {
  try {
    const { query } = req.body;

    if (!query) {
      return res.status(400).json({
        success: false,
        message: "Query required",
      });
    }

    let cases: any[] = [];

    try {
      const { data } = await axios.post(
        "http://127.0.0.1:8000/api/semantic/search",
        { query },
        { timeout: 8000 }
      );
      cases = data?.results || [];
    } catch {
      console.warn("NLP failed, fallback DB search");
    }

    if (!cases.length) {
      cases = await Judgment.find({
        $text: { $search: query },
      }).limit(10);
    }

    if (!cases.length) {
      return res.json({
        success: false,
        message: "No cases found",
      });
    }

    const result = await unifiedLegalAnalysis(cases, query);

    return res.json({
      success: true,
      query,
      ...result,
    });

  } catch (err) {
    console.error("UNIFIED AI ERROR:", err);

    return res.status(500).json({
      success: false,
      message: "Unified analysis failed",
    });
  }
});

// ============================================
// ⚖️ CONFLICT ANALYSIS
// ============================================

router.post("/conflicts", async (req, res) => {
  try {
    const { query } = req.body;

    const { data } = await axios.post(
      "http://127.0.0.1:8000/api/semantic/search",
      { query },
      { timeout: 8000 }
    );

    const cases = data?.results || [];

    if (!cases.length) {
      return res.json({ success: false, message: "No cases found" });
    }

    const analysis = conflictAnalysis(cases);

    return res.json({ success: true, ...analysis });

  } catch (err) {
    console.error("CONFLICT ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// 📄 REPORT GENERATOR
// ============================================

router.post("/report", async (req, res) => {
  try {
    const { query } = req.body;

    const report = await buildLegalReport(query);

    if ((report as any).error) {
      return res.json({ success: false, message: "No data found" });
    }

    const filePath = generatePDF(report);

    return res.download(filePath, () => {
      fs.unlink(filePath, () => {});
    });

  } catch (err) {
    console.error("REPORT ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// 🧾 PETITION GENERATOR
// ============================================

router.post("/petition", async (req, res) => {
  try {
    const { type, facts, query } = req.body;

    const draft = await generatePetition({ type, facts, query });

    if (!draft || typeof draft !== "string") {
      return res.status(400).json({
        success: false,
        message: "Petition generation failed",
      });
    }

    return res.json({ success: true, draft });

  } catch (err) {
    console.error("PETITION ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// 📄 PETITION PDF
// ============================================

router.post("/petition/pdf", async (req, res) => {
  try {
    const { type, facts, query } = req.body;

    const draft = await generatePetition({ type, facts, query });

    if (!draft || typeof draft !== "string") { return res.status(400).json({ success: false, message: "Failed to generate petition" }); }

const filePath = generatePetitionPDF(draft);

    return res.download(filePath, "petition.pdf", () => {
      fs.unlink(filePath, () => {});
    });

  } catch (err) {
    console.error("PETITION PDF ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

// ============================================
// 📂 FULL FILING BUNDLE
// ============================================

router.post("/bundle", async (req, res) => {
  try {
    const filePath = await generateBundlePDF(req.body);

    return res.download(filePath, "filing_bundle.pdf", (err) => {
      if (err) console.error(err);
      fs.unlink(filePath, () => {});
    });

  } catch (err) {
    console.error("BUNDLE ERROR:", err);
    return res.status(500).json({ success: false });
  }
});

export default router;
