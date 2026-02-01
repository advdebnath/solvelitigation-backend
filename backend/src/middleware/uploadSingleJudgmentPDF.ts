import multer from "multer";
import fs from "fs";
import path from "path";

const UPLOAD_DIR = "/var/www/solvelitigation/backend/uploads/judgments";

// Ensure upload directory exists
fs.mkdirSync(UPLOAD_DIR, { recursive: true });

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => {
    cb(null, UPLOAD_DIR);
  },
  filename: (_req, file, cb) => {
    const uniqueName = `${Date.now()}-${file.originalname}`;
    cb(null, uniqueName);
  },
});

const fileFilter: multer.Options["fileFilter"] = (_req, file, cb) => {
  if (file.mimetype !== "application/pdf") {
    return cb(new Error("Only PDF files are allowed"));
  }
  cb(null, true);
};

export const uploadSingleJudgmentPDF = multer({
  storage,
  fileFilter,
  limits: { fileSize: 900 * 1024 * 1024 }, // 50MB
}).single("file");
