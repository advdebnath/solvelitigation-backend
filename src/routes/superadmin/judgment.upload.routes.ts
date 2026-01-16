import express from 'express';
import { uploadJudgments } from '@/controllers/superadmin/judgment.upload.controller';
import { uploadMiddleware } from '@/config/multer';

const router = express.Router();

/**
 * POST /api/superadmin/judgments/upload
 * Upload a judgment document (Supreme Court, High Court, or Tribunal)
 *
 * Form Data:
 * - file: PDF/DOC file
 * - courtType: 'supreme' | 'high' | 'tribunal'
 */
router.post(
  '/upload',
  uploadMiddleware.single('file'),
  uploadJudgments
);

export default router;
