import multer from "multer";
import path from "path";
import fs from "fs";
import { Request } from "express";

/**
 * Root upload directory:
 * uploads/judgments/
 */
const uploadDir = path.join(process.cwd(), "uploads", "judgments");

if (!fs.existsSync(uploadDir)) {
  fs.mkdirSync(uploadDir, { recursive: true });
}

/**
 * Disk storage
 * We DO NOT flatten folders here.
 * webkitRelativePath is preserved in controller.
 */
const storage = multer.diskStorage({
  destination: (_req, _file, cb) => {
    cb(null, uploadDir);
  },

  filename: (_req, file, cb) => {
    const ext = path.extname(file.originalname);
    const base = path.basename(file.originalname, ext);

    const safeBase = base.replace(/[^a-zA-Z0-9_-]/g, "_");
    const unique = `${Date.now()}-${Math.random().toString(36).slice(2, 8)}`;

    cb(null, `${unique}-${safeBase}${ext}`);
  },
});

/**
 * FILE FILTER — FOLDER SAFE
 *
 * RULES:
 * 1️⃣ Ignore directory placeholders
 * 2️⃣ Accept `.pdf`
 * 3️⃣ Silently ignore everything else
 *
 * ❗ NEVER throw for folder upload
 */

function fileFilter(
  _req: Express.Request,
  file: Express.Multer.File,
  cb: multer.FileFilterCallback
) {
  // 1️⃣ Ignore folder placeholders
  if (!file.originalname) {
    return cb(null, false);
  }

  const ext = path.extname(file.originalname).toLowerCase();

  // 2️⃣ Accept ONLY PDFs
  if (ext === ".pdf") {
    return cb(null, true);
  }

  // 3️⃣ Silently ignore everything else
  return cb(null, false);
}



/**
 * EXPORT MIDDLEWARE
 */
export const uploadMiddleware = multer({
  storage,
  fileFilter,
  limits: {
    fileSize: 900 * 1024 * 1024, // 900 MB per file
    files: 5000,                // folder upload support
  },
});
