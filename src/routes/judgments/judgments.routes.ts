import { Router } from "express";
import multer from "multer";
import path from "path";
import { v4 as uuidv4 } from "uuid";

import { listJudgments } from "@/controllers/judgments/judgments.controller";
import {
  getJudgmentsByCourtType,
  downloadJudgment,
  getUploadStats,
  uploadSupremeCourtJudgment,
  uploadHighCourtJudgment,
  uploadTribunalJudgment,
  bulkUploadJudgments,
} from "@/controllers/judgments/upload.controller";

import { authenticateJWT } from "@/middlewares/auth.middleware";
import { enforcePlanLimit } from "@/middlewares/planLimit.middleware";

const router = Router();

/* ===================== VIEW (PLAN LIMITED) ===================== */

router.get(
  "/",
  authenticateJWT,
  enforcePlanLimit("judgmentsViewed"),
  listJudgments
);

router.get(
  "/list/:court",
  authenticateJWT,
  enforcePlanLimit("judgmentsViewed"),
  getJudgmentsByCourtType
);

/* ===================== DOWNLOAD (PLAN LIMITED) ===================== */

router.get(
  "/download/:court/:filename",
  authenticateJWT,
  enforcePlanLimit("downloads"),
  downloadJudgment
);

/* ===================== UPLOAD (ADMIN) ===================== */

const uploadDirs = {
  supremeCourt: path.join(__dirname, "../../uploads/supreme-court"),
  highCourt: path.join(__dirname, "../../uploads/high-court"),
  tribunal: path.join(__dirname, "../../uploads/tribunal"),
};

const storage = multer.diskStorage({
  destination: (req, _file, cb) => {
    const courtType = req.body.courtType || "highCourt";
    let uploadDir = uploadDirs.highCourt;

    if (courtType === "supremeCourt") uploadDir = uploadDirs.supremeCourt;
    else if (courtType === "tribunal") uploadDir = uploadDirs.tribunal;

    cb(null, uploadDir);
  },
  filename: (_req, file, cb) => {
    cb(null, `${uuidv4()}-${file.originalname}`);
  },
});

const upload = multer({
  storage,
  fileFilter: (_req, file, cb) =>
    file.mimetype === "application/pdf"
      ? cb(null, true)
      : cb(new Error("Only PDF files allowed")),
});

/* ===================== STATS ===================== */

router.get("/stats/all", authenticateJWT, getUploadStats);

export default router;
