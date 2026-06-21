import { Router, Request, Response } from "express";
import Judgment from "../models/judgment.model";

const router = Router();

/**

* 🔍 Auto Suggest
  */
  router.get("/", async (req: Request, res: Response) => {
  try {
  const { q } = req.query;

  if (!q || typeof q !== "string") {
  return res.json({
  success: true,
  suggestions: []
  });
  }

  const query = q.trim().toLowerCase();

  if (query.length < 2) {
  return res.json({
  success: true,
  suggestions: []
  });
  }

  const results = await Judgment.find({
  searchText: { $regex: query }
  })
  .select("pointOfLaw")
  .limit(20);

  const suggestions: string[] = [];

  for (const r of results as any[]) {
  for (const p of (r.pointOfLaw || [])) {
  if (
  typeof p === "string" &&
  p.trim().length > 0
  ) {
  suggestions.push(p);
  }
  }
  }

  const uniqueSuggestions =
  Array.from(
    new Set(suggestions)
  ).slice(0, 10);

  return res.json({
  success: true,
  suggestions: uniqueSuggestions
  });

} catch (err) {
console.error("❌ Suggest Error:", err);

return res.status(500).json({
  success: false,
  message: "Suggest failed"
});

}
});

export default router;
