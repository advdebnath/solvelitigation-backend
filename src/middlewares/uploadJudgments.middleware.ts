import multer from "multer";
import path from "path";
import fs from "fs";

const UPLOAD_ROOT = "/var/www/solvelitigation/uploads/judgments";

// ensure base directory exists
fs.mkdirSync(UPLOAD_ROOT, { recursive: true });

const storage = multer.diskStorage({
  destination: (req, file, cb) => {
    cb(null, UPLOAD_ROOT);
  },
  filename: (req, file, cb) => {
    const safeName = file.originalname.replace(/\s+/g, "_");
    cb(null, `${Date.now()}_${safeName}`);
  },
});

export const uploadJudgmentsMiddleware = multer({
  storage,
  limits: {
    fileSize: 900 * 1024 * 1024, // ✅ 900 MB PER FILE
  },
  fileFilter: (_req, file, cb) => {
    if (file.mimetype !== "application/pdf") {
      return cb(new Error("Only PDF files are allowed"));
    }
    cb(null, true);
  },
}).array("files", 50); // up to 50 PDFs in one request
