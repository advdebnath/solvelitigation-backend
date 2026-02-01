import { Request, Response } from "express";
import { Judgment } from "../models/judgment.model";

export const nlpCallback = async (req: Request, res: Response) => {
  try {
    const {
      judgmentId,
      status,
      pointsOfLaw,
      acts,
      category,
      subCategory,
    } = req.body;

    if (!judgmentId) {
      return res.status(400).json({ message: "Missing judgmentId" });
    }

    const update: any = {
      "nlp.status": status || "COMPLETED",
    };

    if (pointsOfLaw) update["nlp.pointsOfLaw"] = pointsOfLaw;
    if (acts) update["nlp.acts"] = acts;

    // ✅ Phase 2.4: persist classification
    if (category) update.category = category;
    if (subCategory) update.subCategory = subCategory;

    const judgment = await Judgment.findByIdAndUpdate(
      judgmentId,
      { $set: update },
      { new: true }
    );

    if (!judgment) {
      return res.status(404).json({ message: "Judgment not found" });
    }

    return res.json({ message: "NLP result saved" });
  } catch (error) {
    console.error("NLP callback error:", error);
    return res.status(500).json({ message: "NLP callback failed" });
  }
};
