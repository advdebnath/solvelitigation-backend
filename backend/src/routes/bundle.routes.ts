import { Router } from "express";
import auth from "../middleware/auth.middleware";
import { generateBundle } from "../services/bundle.service";

const router = Router();

// ============================================
// 🔥 GENERATE FULL BUNDLE
// ============================================

router.get("/:caseId", auth, async (req, res) => {
  try {
    const data = await generateBundle(req.params.caseId);

    res.json({ success: true, data });

  } catch (err) {
    console.error(err);
    res.status(500).json({ success: false });
  }
});

export default router;
