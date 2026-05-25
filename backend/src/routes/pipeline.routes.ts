import { Router } from "express";
import multer from "multer";
import fs from "fs";
import axios from "axios";
import path from "path";
import { execSync } from "child_process";

import CaseContext from "../models/caseContext.model";
import auth from "../middleware/auth.middleware";
import { generateLegalAnalysis } from "../services/reasoning.service";
import { generatePetitionDraft } from "../services/drafting.service";
import { generateStrategy } from "../services/strategy.service";
import { buildCitationArgument } from "../services/citation.service";
import { generateFinalArguments } from "../services/finalArgument.service";
import { generateWrittenSubmissions } from "../services/submission.service";
import { generateCrossExamination } from "../services/crossExamination.service";
import { generateAppealDraft } from "../services/appeal.service";

const router = Router();

const upload = multer({
  dest: "/var/www/solvelitigation/backend/uploads/temp",
  limits: {
    fileSize: 50 * 1024 * 1024,
  },
});

const NLP_URL = process.env.NLP_URL || "http://127.0.0.1:8000";

// ============================================
// 🔥 SAFE EXEC
// ============================================

const safeExec = (cmd: string) => {
  try {
    if (!cmd) throw new Error("Invalid command");

    execSync(cmd, {
      stdio: "ignore",
      timeout: 10000,
      maxBuffer: 10 * 1024 * 1024,
    });

    return true;
  } catch (err: any) {
    console.error("❌ safeExec error:", err.message);
    return false;
  }
};

// ============================================
// 🔥 CLEAN TEXT
// ============================================

const cleanText = (text: string) => {
  return text
    .replace(/<[^>]+>/g, " ")
    .replace(/[^a-zA-Z0-9\s.,:;()\-\/]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
};

// ============================================
// 🔥 CASE LAW FETCH
// ============================================

const fetchCaseLaws = async (query: string) => {
  try {
    const { data } = await axios.post(`${NLP_URL}/faiss/search`, {
      text: query,
    });

    if (!data.success) return [];

    return data.results.slice(0, 3);
  } catch (err) {
    console.error("❌ Case-law fetch error:", err);
    return [];
  }
};

// ============================================
// 🔥 TEXT EXTRACTION
// ============================================

const extractText = (filePath: string): string => {
  const ext = path.extname(filePath).toLowerCase();
  let text = "";

  try {
    if (ext === ".txt") {
      text = fs.readFileSync(filePath, "utf-8");
    } else if (ext === ".pdf") {
      let extracted = "";

      const txtPath = filePath + ".txt";

      if (safeExec(`pdftotext "${filePath}" "${txtPath}"`) && fs.existsSync(txtPath)) {
        extracted = fs.readFileSync(txtPath, "utf-8");
        fs.unlinkSync(txtPath);
      }

      const isGarbage =
        !extracted ||
        extracted.length < 50 ||
        extracted.includes("stream");

      if (isGarbage) {
        console.log("⚡ OCR fallback...");

        const base = filePath.replace(".pdf", "");
        const imgPrefix = base + "_page";

        safeExec(`pdftoppm -png -r 300 "${filePath}" "${imgPrefix}"`);

        const dir = path.dirname(filePath);
        const files = fs.readdirSync(dir);

        let combined = "";

        for (const f of files) {
          if (f.startsWith(path.basename(imgPrefix)) && f.endsWith(".png")) {
            const imgPath = path.join(dir, f);
            const outBase = imgPath.replace(".png", "");

            safeExec(`tesseract "${imgPath}" "${outBase}" -l eng --psm 6`);

            const ocrTxt = outBase + ".txt";

            if (fs.existsSync(ocrTxt)) {
              combined += fs.readFileSync(ocrTxt, "utf-8") + " ";
              fs.unlinkSync(ocrTxt);
            }

            fs.unlinkSync(imgPath);
          }
        }

        extracted = combined;
      }

      text = extracted;
    } else {
      text = fs.readFileSync(filePath, "utf-8");
    }
  } catch (err) {
    console.error("❌ EXTRACTION ERROR:", err);
    text = "";
  }

  return cleanText(text);
};

// ============================================
// 🔥 FULL PIPELINE
// ============================================

router.post("/upload-case", auth, upload.single("file"), async (req: any, res) => {
  let filePath = "";

  try {
    const file = req.file;

    if (!file) {
      return res.status(400).json({ success: false, message: "File not uploaded" });
    }

    filePath = file.path;

    const text = extractText(filePath);

    if (!text || text.length < 30) {
      return res.status(400).json({
        success: false,
        message: "Invalid or unreadable document",
      });
    }

    // NLP
    const { data } = await axios.post(`${NLP_URL}/api/extract-facts`, { text });

    if (!data.success) {
      return res.status(500).json({ success: false, message: "Fact extraction failed" });
    }

    const facts = data.data;

    // ANALYSIS
    const analysis = generateLegalAnalysis(facts.facts || "");

    // CASE LAW
    const caseLaws = await fetchCaseLaws(facts.facts || "");

    const finalArgument = buildCitationArgument(analysis.arguments, caseLaws);

    const caseId = `CASE-${Date.now()}`;

    const context = await CaseContext.create({
      caseId,
      court: "HIGH COURT",
      caseType: "WRIT",
      petitioner: facts.petitioner || "Petitioner",
      respondent: facts.respondent || "Respondent",
      facts: facts.facts || "",
      grounds: analysis.grounds,
      prayer: facts.relief || "",
    });

    // GENERATORS
    const draft = generatePetitionDraft(context, analysis, caseLaws);
    const strategy = generateStrategy(analysis);
    const finalArguments = generateFinalArguments(analysis, caseLaws);
    const writtenSubmissions = generateWrittenSubmissions(context, analysis, caseLaws);

    // 🔥 NEW ENGINES
    const crossExamination = generateCrossExamination(facts.facts, analysis);
    const appealDraft = generateAppealDraft(context, analysis, "Impugned order details");

    return res.json({
      success: true,
      caseId,
      extracted: facts,
      analysis: { ...analysis, arguments: finalArgument },
      caseLaws,
      strategy,
      draft,
      finalArguments,
      writtenSubmissions,
      crossExamination,
      appealDraft,
      context,
    });

  } catch (err: any) {
    console.error("❌ PIPELINE ERROR:", err.message);

    return res.status(500).json({
      success: false,
      message: "Pipeline failed",
    });

  } finally {
    if (filePath && fs.existsSync(filePath)) {
      fs.unlinkSync(filePath);
    }
  }
});

export default router;
