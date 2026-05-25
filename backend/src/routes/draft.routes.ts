import { Router } from "express";
import auth from "../middleware/auth.middleware";

// ✅ CORRECT SERVICE
import {
  saveFinalDraft,
  getDraftsByCase,
  getDraftById,
  updateDraft,
  deleteDraft,
} from "../services/draft.service";

import { generatePetitionDraft } from "../services/drafting.service";

const router = Router();

// ============================================
// 🔥 SAVE FINAL
// ============================================

router.post("/save", auth, async (req: any, res) => {
  try {
    const draft = await saveFinalDraft(req.body, req.user.id);
    res.json({ success: true, draft });
  } catch (err) {
    console.error("❌ SAVE ERROR:", err);
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 AI REWRITE (NEW FEATURE)
// ============================================

router.post("/rewrite", auth, async (req: any, res) => {
  try {
    const { context, analysis } = req.body;

    const draft = generatePetitionDraft(context, analysis);

    res.json({
      success: true,
      draft,
    });
  } catch (err) {
    console.error("❌ REWRITE ERROR:", err);
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 GET BY CASE
// ============================================

router.get("/case/:caseId", auth, async (req: any, res) => {
  try {
    const drafts = await getDraftsByCase(req.params.caseId);
    res.json({ success: true, drafts });
  } catch (err) {
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 GET SINGLE
// ============================================

router.get("/:id", auth, async (req: any, res) => {
  try {
    const draft = await getDraftById(req.params.id);
    res.json({ success: true, draft });
  } catch {
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 UPDATE
// ============================================

router.put("/:id", auth, async (req: any, res) => {
  try {
    const draft = await updateDraft(req.params.id, req.body.content);
    res.json({ success: true, draft });
  } catch {
    res.status(500).json({ success: false });
  }
});

// ============================================
// 🔥 DELETE
// ============================================

router.delete("/:id", auth, async (req: any, res) => {
  try {
    await deleteDraft(req.params.id);
    res.json({ success: true });
  } catch {
    res.status(500).json({ success: false });
  }
});

export default router;
