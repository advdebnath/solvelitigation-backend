import { Router } from "express";
import axios from "axios";

const router = Router();

// ============================================
// 🔥 CONFIG
// ============================================

const NLP_URL =
  process.env.NLP_SERVICE_URL || "http://localhost:8000";

// ============================================
// 🔥 SAFE TEXT CLEANER
// ============================================

const sanitizeText = (text: string) => {
  return text
    .replace(/[^a-zA-Z0-9\s.,\-]/g, "") // remove unsafe chars
    .replace(/\s+/g, " ")               // normalize spaces
    .trim()
    .slice(0, 300);                    // limit length
};

// ============================================
// 🔥 STUDENT ANSWER API (SECURE + LIMITED)
// ============================================

router.post("/answer", async (req: any, res) => {
  try {
    // ============================================
    // 🔥 ROLE CHECK
    // ============================================

    if (!req.user || req.user.role !== "simple") {
      return res.status(403).json({
        success: false,
        message: "Student access only",
      });
    }

    // ============================================
    // 🔥 INPUT VALIDATION
    // ============================================

    let { text } = req.body;

    if (!text || typeof text !== "string") {
      return res.status(400).json({
        success: false,
        message: "Invalid input",
      });
    }

    text = sanitizeText(text);

    if (text.length < 3) {
      return res.status(400).json({
        success: false,
        message: "Query too short",
      });
    }

    // ============================================
    // 🔥 CALL NLP SERVICE
    // ============================================

    const response = await axios.post(
      `${NLP_URL}/api/student-answer`,
      { text },
      {
        timeout: 8000,
      }
    );

    const data = response?.data || {};

    // ============================================
    // 🔥 SAFE RESPONSE FILTER
    // ============================================

    const safeResponse = {
      success: data.success === false ? false : true,
      answer:
        typeof data.answer === "string" && data.answer.length > 0
          ? data.answer
          : "No answer available",
      source: Array.isArray(data.source)
        ? data.source.slice(0, 3)
        : [],
    };

    return res.json(safeResponse);

  } catch (err: any) {
    // ============================================
    // 🔥 ERROR HANDLING (IMPROVED)
    // ============================================

    console.error("❌ Student API Error:");
    console.error("Message:", err?.message);
    console.error("URL:", `${NLP_URL}/api/student-answer`);
    console.error("Stack:", err?.stack);

    if (err.code === "ECONNREFUSED") {
      return res.status(500).json({
        success: false,
        message: "NLP service not reachable",
      });
    }

    if (err.code === "ECONNABORTED") {
      return res.status(500).json({
        success: false,
        message: "NLP service timeout",
      });
    }

    return res.status(500).json({
      success: false,
      message: "Student service unavailable",
    });
  }
});

export default router;
