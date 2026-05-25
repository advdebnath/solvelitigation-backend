import { Router, Request, Response } from "express";
import Judgment from "../models/judgment.model";

const router = Router();

/**
 * 🔍 Auto Suggest (FINAL VERSION)
 */
router.get("/", async (req: Request, res: Response) => {
  try {
    const { q } = req.query;

    if (!q || typeof q !== "string") {
      return res.json({ success: true, suggestions: [] });
    }

    const query = q.trim().toLowerCase();

    if (query.length < 2) {
      return res.json({ success: true, suggestions: [] });
    }

    const results = await Judgment.find({
      searchText: { $regex: query }
    })
      .select("pointOfLaw")
      .limit(20);

    const suggestions = [
      ...new Set(
        results
          .map((r) => r.pointOfLaw)
          .filter((p) => typeof p === "string" && p.trim().length > 0)
      )
    ].slice(0, 10);

    res.json({
      success: true,
      suggestions
    });

  } catch (err) {
    console.error("❌ Suggest Error:", err);
    res.status(500).json({
      success: false,
      message: "Suggest failed"
    });
  }
});

export default router;
