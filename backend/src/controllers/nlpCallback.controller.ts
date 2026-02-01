import { Request, Response } from "express";
import { Judgment } from "../models/judgment.model";
import { AuditLog } from "../models/auditLog.model";

export const nlpCallback = async (req: Request, res: Response) => {
  try {
    const {
      lockId,
      status,
      category,
      subCategory,
      pointsOfLaw,
      acts,
      error,
    } = req.body;

    if (!lockId) {
      return res.status(400).json({ message: "lockId required" });
    }

    const update: any = {
      "nlp.status": status,
      "nlp.completedAt": new Date(),
    };

    if (pointsOfLaw) update["nlp.pointsOfLaw"] = pointsOfLaw;
    if (acts) update["nlp.acts"] = acts;
    if (error) update["nlp.lastError"] = error;

    const judgment = await Judgment.findOneAndUpdate(
      { "nlp.lockId": lockId },   // ✅ FIX
      { $set: update },
      { new: true }
    );

    if (!judgment) {
      return res.status(404).json({ message: "Judgment not found" });
    }

    await AuditLog.create({
      action: "NLP_CALLBACK",
      entity: "Judgment",
      entityId: judgment._id,
      meta: req.body,
    });

    return res.json({ success: true });
  } catch (err) {
    console.error("NLP CALLBACK ERROR:", err);
    return res.status(500).json({ message: "Callback failed" });
  }
};
