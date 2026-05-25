import { Request, Response } from "express";
import Judgment from "../models/judgment.model";
import { buildJudgmentQuery } from "../services/judgmentQueryBuilder.service";

// ============================================
// 📋 GET ALL JUDGMENTS (RBAC SAFE)
// ============================================
export const getAllJudgments = async (req: any, res: any) => {
  try {
    const { filter, page, limit, skip, sort } = buildJudgmentQuery(
      req.query as any
    );

    // 🔐 RBAC FILTER (CRITICAL)
    if (!["superadmin", "editor"].includes(req.user?.role)) {
      filter.status = "APPROVED"; // only approved for normal users
    }

    const total = await Judgment.countDocuments(filter);

    const query = Judgment.find(filter)
      .select(
        "caseNumber judgmentDate category court confidence pageCount createdAt status"
      )
      .sort(sort)
      .skip(skip)
      .limit(limit)
      .lean();

    const judgments = await query;

    return res.json({
      success: true,
      data: judgments,
      pagination: {
        total,
        page,
        totalPages: Math.ceil(total / limit),
        limit,
        hasNextPage: page < Math.ceil(total / limit),
        hasPrevPage: page > 1,
      },
    });
  } catch (error) {
    console.error("Error fetching judgments:", error);
    return res.status(500).json({
      success: false,
      message: "Failed to fetch judgments",
    });
  }
};

// ============================================
// 🔐 REVIEW JUDGMENT
// ============================================
export const reviewJudgment = async (req: any, res: any) => {
  try {
    const { id } = req.params;

    const judgment = await Judgment.findById(id);
    if (!judgment) {
      return res.status(404).json({ success: false, message: "Not found" });
    }

    if (judgment.status !== "EXTRACTED") {
      return res.status(400).json({
        success: false,
        message: "Only EXTRACTED judgments can be reviewed",
      });
    }

    const { headnote, pointsOfLaw, actReferences, parties } = req.body;

    if (headnote) judgment.headnote = headnote;
    if (pointsOfLaw) judgment.pointsOfLaw = pointsOfLaw;
    if (actReferences) judgment.actReferences = actReferences;
    if (parties) judgment.parties = parties;

    judgment.status = "REVIEWED";
    judgment.reviewedBy = req.user.id;
    judgment.reviewedAt = new Date();

    await judgment.save();

    return res.json({ success: true, data: judgment });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Review failed" });
  }
};

// ============================================
// 🔐 APPROVE JUDGMENT
// ============================================
export const approveJudgment = async (req: any, res: any) => {
  try {
    const { id } = req.params;

    const judgment = await Judgment.findById(id);
    if (!judgment) {
      return res.status(404).json({ success: false, message: "Not found" });
    }

    if (judgment.status !== "REVIEWED") {
      return res.status(400).json({
        success: false,
        message: "Only REVIEWED judgments can be approved",
      });
    }

    judgment.status = "APPROVED";
    judgment.approvedBy = req.user.id;
    judgment.approvedAt = new Date();

    await judgment.save();

    return res.json({ success: true, data: judgment });
  } catch (err) {
    return res.status(500).json({ success: false, message: "Approval failed" });
  }
};

// ============================================
// 📋 ADMIN LIST BY STATUS
// ============================================
export const getJudgmentsByStatus = async (req: any, res: any) => {
  try {
    const status = req.query.status || "EXTRACTED";

    const judgments = await Judgment.find({ status })
      .select("headnote category status createdAt")
      .sort({ createdAt: -1 })
      .limit(50);

    return res.json({
      success: true,
      count: judgments.length,
      data: judgments,
    });
  } catch (err) {
    return res.status(500).json({
      success: false,
      message: "Failed to fetch judgments",
    });
  }
};
