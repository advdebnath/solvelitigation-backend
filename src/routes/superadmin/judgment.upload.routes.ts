import { Router } from "express";
import multer from "multer";
import { uploadJudgment } from "../../controllers/superadmin/judgment.upload.controller";

const router = Router();

/**
 * GridFS MUST use memoryStorage
 */
const upload = multer({
  storage: multer.memoryStorage(),
  limits: {
    fileSize: 1024 * 1024 * 1024, // 1 GB
  },
});

router.post("/", upload.single("file"), uploadJudgment);

export default router;
