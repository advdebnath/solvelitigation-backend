import multer from "multer";

const storage = multer.memoryStorage();

export const pdfUpload = multer({
  storage,
  limits: {
    fileSize: 900 * 1024 * 1024, // 900 MB
  },
  fileFilter: (_, file, cb) => {
    if (file.mimetype !== "application/pdf") {
      cb(new Error("Only PDF files allowed"));
    } else {
      cb(null, true);
    }
  },
});
