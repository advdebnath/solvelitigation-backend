import { Request, Response } from "express";
import mongoose from "mongoose";
import { Judgment } from "../models";

export const getJudgmentById = async (req: Request, res: Response) => {
  try {
    const { id } = req.params;

    if (!mongoose.Types.ObjectId.isValid(id)) {
      return res.status(400).json({ message: "Invalid judgment ID" });
    }

    const judgment = await Judgment.findById(id).select(
      "title year category subCategory status nlp uploadedAt"
    );

    if (!judgment) {
      return res.status(404).json({ message: "Judgment not found" });
    }

    res.json(judgment);
  } catch (error) {
    console.error("❌ getJudgmentById error:", error);
    res.status(500).json({ message: "Internal server error" });
  }
};
