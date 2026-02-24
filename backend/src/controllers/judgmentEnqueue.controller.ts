import { Request, Response } from "express";
import { Types } from "mongoose";
import axios from "axios";
import Judgment from "../models/judgment.model";
import JudgmentIngestion from "../models/JudgmentIngestion";

export const enqueueJudgmentNlp = async (req: Request, res: Response) => {
  try {
    const { judgmentId } = req.params;

    if (!Types.ObjectId.isValid(judgmentId)) {
      return res.status(400).json({ message: "Invalid judgmentId" });
    }

    const judgment = await Judgment.findById(judgmentId);

    if (!judgment) {
      return res.status(404).json({ message: "Judgment not found" });
    }

    // 🔍 Find related ingestion
    const ingestion = await JudgmentIngestion.findOne({
      judgmentId: judgment._id,
    });

    if (!ingestion) {
      return res.status(404).json({
        message: "Related ingestion not found",
      });
    }

    if (judgment.nlpStatus !== "QUEUED") {
      return res.status(400).json({
        message: "Judgment is not in QUEUED state",
      });
    }

    // 🔒 Atomic state transition
    judgment.nlpStatus = "PROCESSING";
await Judgment.updateOne(
  { _id: judgment._id },
  { $set: { nlpStatus: "QUEUED" } },
  { runValidators: false }
);


    // 🚀 Call NLP service with ingestionId
    await axios.post("http://127.0.0.1:8000/api/enqueue", {
      ingestionId: ingestion._id.toString(),
    });

    return res.json({
      success: true,
      message: "Judgment sent to NLP service",
    });

  } catch (err: any) {
    console.error(
      "Direct NLP enqueue error:",
      err.response?.data || err.message
    );
    return res.status(500).json({ message: "Internal server error" });
  }
};
