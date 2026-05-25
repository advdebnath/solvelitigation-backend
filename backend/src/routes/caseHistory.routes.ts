import express from "express";
import CaseHistory from "../models/CaseHistory";

const router = express.Router();

// SAVE CASE
router.post("/save", async (req, res) => {
  try {
    const data = await CaseHistory.create(req.body);
    res.json({ success: true, data });
  } catch (err) {
    res.status(500).json({ success: false, error: err });
  }
});

// GET ALL CASES
router.get("/", async (req, res) => {
  const data = await CaseHistory.find().sort({ createdAt: -1 });
  res.json({ success: true, data });
});

export default router;
