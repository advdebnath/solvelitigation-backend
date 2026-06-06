import { Request, Response } from "express";
import JudgmentIngestion from "../../models/JudgmentIngestion";
import Judgment from "../../models/judgment.model";
import { io } from "../../server";

import { calculatePages } from "../../utils/pageCalculator";
import { generateSLSC } from "../../utils/slscGenerator";

import {
  cleanText,
  extractParties,
  cleanPointsOfLaw,
  detectCategory,
  extractLegalPoints,
  extractActsAndSections,
} from "../../utils/legalProcessor";

import { generateHeadnote } from "../../utils/headnoteGenerator";

// 🔥 NEW (IMPORTANT)
import { mapPointsToLaw } from "../../utils/lawMapper";

// ============================================
// 🔥 NLP CALLBACK CONTROLLER (FINAL PRODUCTION)
// ============================================

export const nlpCallbackController = async (
  req: Request,
  res: Response
): Promise<Response> => {
  try {
    const { ingestionId, status, result, error } = req.body;

    if (!ingestionId || !status) {
      return res.status(400).json({
        success: false,
        message: "Invalid callback payload",
      });
    }

    const ingestion = await JudgmentIngestion.findById(ingestionId);

    if (!ingestion) {
      return res.status(404).json({
        success: false,
        message: "Ingestion not found",
      });
    }

    if (ingestion.status === "COMPLETED" && status === "COMPLETED") {
      return res.json({ success: true });
    }

    // ============================================
    // PROCESSING
    // ============================================
    if (status === "PROCESSING") {
      ingestion.status = "PROCESSING";
      await ingestion.save();

      io.emit("ingestion-status-updated", {
        ingestionId,
        status: "PROCESSING",
      });

      return res.json({ success: true });
    }

    // ============================================
    // COMPLETED
    // ============================================
    if (status === "COMPLETED") {
      ingestion.status = "COMPLETED";
      ingestion.completedAt = new Date();
      ingestion.nlpUpdatedAt = new Date();
      await ingestion.save();

      // ============================================
      // TEXT
      // ============================================

      const rawText =
        result?.cleanedText ||
        result?.text ||
        result?.htmlContent ||
        "";

      const fullText = cleanText(rawText);

      const pageCount =
        result?.pageCount && result.pageCount > 0
          ? result.pageCount
          : calculatePages(fullText);

      const year = result?.judgmentDate
        ? new Date(result.judgmentDate).getFullYear()
        : new Date().getFullYear();

      const slscData = await generateSLSC(year, pageCount);

      // ============================================
      // 🔥 LEGAL INTELLIGENCE
      // ============================================

      const parties = extractParties(fullText);

      const nlpPoints = cleanPointsOfLaw(result?.pointsOfLaw || []);
      const fallbackPoints = extractLegalPoints(fullText);

      const finalPoints = [
        ...new Set([...nlpPoints, ...fallbackPoints]),
      ];

      const category =
        result?.category || detectCategory(fullText);

      // ============================================
      // 🔥 🔥 LAW MAPPING (CORE FIX)
      // ============================================

      const lawMapping = mapPointsToLaw(finalPoints);

      const extracted = extractActsAndSections(fullText);

      const acts =
        lawMapping.acts.length > 0
          ? lawMapping.acts
          : extracted.acts;

      const sections =
        lawMapping.sections.length > 0
          ? lawMapping.sections
          : extracted.sections;

      const sectionActMap = lawMapping.sectionActMap;

      // ============================================
      // 🔥 HEADNOTE
      // ============================================

      const headnote = generateHeadnote(fullText);

      // 🔥 IMPROVED STRUCTURED HEADNOTES
      const headnotes = finalPoints.map((point: string) => ({
        issue: `Whether ${point} is established?`,
        rule: `Legal principles governing ${point}`,
        application: "",
        conclusion: headnote,
      }));

      // ============================================
      // 🔥 SAVE
      // ============================================

      await Judgment.findOneAndUpdate(
        { ingestionId: ingestion._id },
        {
          $set: {
            ingestionId: ingestion._id,

            caseNumber: result?.caseNumber || "UNKNOWN",

            category,
            subCategory: result?.subCategory || null,

            fullText,

            acts,
            sections,
            sectionActMap, // 🔥 NEW

            pointOfLaw: finalPoints,

            headnote,
            headnotes,

            parties,

            summary: result?.summary || "",
            confidence: result?.confidence || 0,

            slscCitation: slscData.slscCitation,
            startPage: slscData.startPage,
            endPage: slscData.endPage,
            pageCount: slscData.pageCount,

            checksum: ingestion.file?.sha256 || null,
            nlpStatus: "COMPLETED",
            updatedAt: new Date(),
          },
        },
        { upsert: true, new: true }
      );

      io.emit("judgment:update", { ingestionId });

      io.emit("ingestion-status-updated", {
        ingestionId,
        status: "COMPLETED",
      });

      await JudgmentIngestion.updateOne(
        { _id: ingestion._id },
        {
          $set: {
            status: "COMPLETED",
            stage: "COMPLETED",
            isCompleted: true,
            completedAt: new Date(),
            error: null,
            nlpProcessed: true,
          },
        }
      );

      return res.json({ success: true });
    }

    // ============================================
    // FAILED
    // ============================================
    if (status === "FAILED") {
      ingestion.status = "FAILED";
      ingestion.error = error || "Unknown NLP failure";
      await ingestion.save();

      return res.json({ success: true });
    }

    return res.status(400).json({
      success: false,
      message: "Invalid status",
    });

  } catch (err) {
    console.error("❌ NLP Callback Error:", err);

    return res.status(500).json({
      success: false,
      message: "Internal server error",
    });
  }
};
