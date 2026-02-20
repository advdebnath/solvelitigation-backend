import { Request, Response } from "express";
import { Types } from "mongoose";
import axios from "axios";
import Judgment from "../models/judgment.model";

export const enqueueJudgmentNlp = async (req: Request, res: Response) => {
  try {
    const { judgmentId } = req.params;

    if (!Types.ObjectId.isValid(judgmentId)) {
      return res.status(400).json({ message: "Invalid judgmentId" });
    }

    // 🔒 Atomic state transition: only QUEUED → PROCESSING
    const updated = await Judgment.findOneAndUpdate(
      { _id: judgmentId, nlpStatus: "QUEUED" },
      { $set: { nlpStatus: "PROCESSING" } },
      { new: true }
    );

    if (!updated) {
      return res.status(400).json({
        message: "Judgment is not in QUEUED state",
      });
    }

    // 🚀 Call NLP service
    await axios.post("http://127.0.0.1:8000/api/enqueue", {
      judgmentId: updated._id.toString(),
    });

    return res.json({
      success: true,
      message: "Judgment sent to NLP service",
    });

  } catch (err: any) {
    console.error("Direct NLP enqueue error:", err.message);
    return res.status(500).json({ message: "Internal server error" });
  }
};
