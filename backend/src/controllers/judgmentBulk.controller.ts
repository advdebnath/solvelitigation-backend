import fs from "fs";
import path from "path";
import axios from "axios";
import { Request, Response } from "express";

import { Judgment } from "../models/judgment.model";
import { saveFileToGridFS } from "../utils/saveToGridFS";
import { extractDateFromFilename } from "../utils/extractDateFromFilename";
import { UploadAudit } from "../models/uploadAudit.model";



const INBOX = "/data/judgments/inbox";
const PROCESSED = "/data/judgments/processed";
const FAILED = "/data/judgments/failed";

/**
 * Extract YEAR / MONTH / DATE from folder path:
 * /data/judgments/inbox/2026/01/28/file.pdf
 */
const extractDateFromPath = (filePath: string) => {
  const parts = filePath.split("/");

  if (parts.length < 4) return null;

  const date = Number(parts[parts.length - 2]);
  const month = Number(parts[parts.length - 3]);
  const year = Number(parts[parts.length - 4]);

  if (
    year >= 1900 &&
    month >= 1 && month <= 12 &&
    date >= 1 && date <= 31
  ) {
    return { year, month, date };
  }

  return null;
};

/**
 * Recursively scan inbox for PDFs
 */
const scanPdfFiles = (dir: string): string[] => {
  let results: string[] = [];

  if (!fs.existsSync(dir)) return results;

  for (const entry of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, entry);

    if (fs.statSync(fullPath).isDirectory()) {
      results = results.concat(scanPdfFiles(fullPath));
    } else if (entry.toLowerCase().endsWith(".pdf")) {
      results.push(fullPath);
    }
  }

  return results;
};

/**
 * POST /api/judgments/upload-bulk
 * ADMIN / SUPERADMIN only
 */
export const uploadBulkFromInbox = async (req: Request, res: Response) => {
  const { courtType = "SUPREME_COURT", category = "CRIMINAL" } = req.body || {};

  const files = scanPdfFiles(INBOX);

  let uploaded = 0;
  let failed = 0;
  const errors: any[] = [];

  for (const fullPath of files) {
    const file = path.basename(fullPath);

    try {
      /** 1️⃣ Resolve judgment date */
      const folderDate = extractDateFromPath(fullPath);
      const fileDate = extractDateFromFilename(file);
      const now = new Date();

      const year = folderDate?.year ?? fileDate?.year ?? now.getFullYear();
      const month = folderDate?.month ?? fileDate?.month ?? now.getMonth() + 1;
      const date = folderDate?.date ?? fileDate?.date ?? now.getDate();

      /** 2️⃣ Save PDF to GridFS */
      const stream = fs.createReadStream(fullPath);
      const gridfsFileId = await saveFileToGridFS(stream, file);


/** 3️⃣ Create judgment record */
const judgment = await Judgment.create({
  title: `${courtType} ${category} Judgment (${year}-${month}-${date})`,
  courtType,
  category,
  year,
  month,
  date,
  gridfsFileId,
  originalFileName: file,
  uploadedBy: req.currentUser?._id || null,
  status: "UPLOADED",
  nlp: {
    status: "PROCESSING",
    pointsOfLaw: [],
    acts: [],
  },
});

/** 3️⃣a Audit log (AFTER judgment exists) */
await UploadAudit.create({
  judgmentId: judgment._id,
  fileName: file,
  action: "UPLOAD_BULK",
  uploadedBy: req.currentUser!._id,
  ip: req.ip,
  userAgent: req.headers["user-agent"],
});

      /** 4️⃣ Enqueue NLP */
      await axios.post("http://127.0.0.1:8000/enqueue", {
        jobId: judgment._id.toString(),
        pdfPath: fullPath,
      });

      /** 5️⃣ Move to processed folder */
      const targetDir = path.join(
        PROCESSED,
        String(year),
        String(month).padStart(2, "0"),
        String(date).padStart(2, "0")
      );

      fs.mkdirSync(targetDir, { recursive: true });
      fs.renameSync(fullPath, path.join(targetDir, file));

      uploaded++;
    } catch (err: any) {
      /** 6️⃣ Move to failed folder */
      const targetDir = path.join(FAILED, "unknown");
      fs.mkdirSync(targetDir, { recursive: true });

      try {
        fs.renameSync(fullPath, path.join(targetDir, file));
      } catch {}

      failed++;
      errors.push({
        file,
        error: err?.message || "Unknown error",
      });
    }
  }

  return res.json({
    success: true,
    scanned: files.length,
    uploaded,
    failed,
    errors,
  });
};
