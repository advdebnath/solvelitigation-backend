import axios from "axios";
import { Request, Response } from "express";
import { Judgment } from "../models/judgment.model";

export const retryNLP = async (req: Request, res: Response) => {
  const { judgmentId } = req.params;

  const judgment = await Judgment.findById(judgmentId);
  if (!judgment) {
    return res.status(404).json({ message: "Judgment not found" });
  }

  try {
    await axios.post("http://127.0.0.1:8000/enqueue", {
      jobId: judgment._id.toString(),
    });

    judgment.nlp.status = "PROCESSING";
    await judgment.save();

    return res.json({
      success: true,
      status: "REQUEUED",
    });
  } catch (error) {
    return res.status(503).json({
      success: false,
      message: "NLP service unavailable",
    });
  }
};
