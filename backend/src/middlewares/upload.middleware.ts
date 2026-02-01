import multer from "multer";

const storage = multer.diskStorage({
  destination: (_req, _file, cb) => {
    cb(null, "/tmp"); // temp storage (ideal for large PDFs)
  },
  filename: (_req, file, cb) => {
    const unique = Date.now() + "-" + Math.round(Math.random() * 1e9);
    cb(null, `${unique}-${file.originalname}`);
  },
});

const upload900MB = multer({
  storage,
  limits: {
    fileSize: 900 * 1024 * 1024, // 900 MB
  },
  fileFilter: (_req, file, cb) => {
    if (file.mimetype !== "application/pdf") {
      cb(new Error("Only PDF files are allowed"));
    } else {
      cb(null, true);
    }
  },
});

/**
 * ✅ Single judgment upload (used by route)
 */
export const uploadSingleJudgmentPDF = upload900MB.single("file");

/**
 * (Optional future use)
 * export const uploadMultipleJudgments = upload900MB.array("files", 50);
 */

export { upload900MB };
