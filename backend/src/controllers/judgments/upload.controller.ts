import { Request, Response } from "express";
import fs from "fs";
import path from "path";
import { validateJudgmentPath } from "../../utils/folderValidator";
import { v4 as uuidv4 } from "uuid";

const uploadDirs = {
  supremeCourt: path.join(__dirname, "../../uploads/supreme-court"),
  highCourt: path.join(__dirname, "../../uploads/high-court"),
  tribunal: path.join(__dirname, "../../uploads/tribunal"),
};

Object.values(uploadDirs).forEach((dir) => {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
});

export const uploadSupremeCourtJudgment = (req: Request, res: Response) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: "No file uploaded" });
    res.status(200).json({
      success: true,
      message: "Supreme Court judgment uploaded successfully",
      data: {
        id: uuidv4(),
        fileName: req.file.filename,
        originalName: req.file.originalname,
        fileSize: req.file.size,
        fileSizeMB: (req.file.size / (1024 * 1024)).toFixed(2),
        court: "Supreme Court",
        caseNumber: req.body.caseNumber,
        caseTitle: req.body.caseTitle,
        uploadedAt: new Date().toISOString(),
      },
    });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const uploadHighCourtJudgment = (req: Request, res: Response) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: "No file uploaded" });
    res.status(200).json({
      success: true,
      message: "High Court judgment uploaded successfully",
      data: {
        id: uuidv4(),
        fileName: req.file.filename,
        originalName: req.file.originalname,
        fileSize: req.file.size,
        fileSizeMB: (req.file.size / (1024 * 1024)).toFixed(2),
        court: "High Court",
        caseNumber: req.body.caseNumber,
        caseTitle: req.body.caseTitle,
        uploadedAt: new Date().toISOString(),
      },
    });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const uploadTribunalJudgment = (req: Request, res: Response) => {
  try {
    if (!req.file) return res.status(400).json({ success: false, message: "No file uploaded" });
    res.status(200).json({
      success: true,
      message: "Tribunal judgment uploaded successfully",
      data: {
        id: uuidv4(),
        fileName: req.file.filename,
        originalName: req.file.originalname,
        fileSize: req.file.size,
        fileSizeMB: (req.file.size / (1024 * 1024)).toFixed(2),
        court: "Tribunal",
        caseNumber: req.body.caseNumber,
        caseTitle: req.body.caseTitle,
        uploadedAt: new Date().toISOString(),
      },
    });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const bulkUploadJudgments = (req: Request, res: Response) => {
  try {
    if (!req.files || (Array.isArray(req.files) && req.files.length === 0)) {
      return res.status(400).json({ success: false, message: "No files uploaded" });
    }
    const files = Array.isArray(req.files) ? req.files : [req.files];
    const totalSize = files.reduce((sum: number, f: any) => sum + f.size, 0);
    res.status(200).json({
      success: true,
      message: `${files.length} files uploaded successfully`,
      totalFiles: files.length,
      totalSizeMB: (totalSize / (1024 * 1024)).toFixed(2),
    });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const getJudgmentsByCourtType = (req: Request, res: Response) => {
  try {
    const court = req.params.court;
    let uploadDir = uploadDirs.highCourt;
    if (court === "supreme-court") uploadDir = uploadDirs.supremeCourt;
    else if (court === "tribunal") uploadDir = uploadDirs.tribunal;
    const files = fs.readdirSync(uploadDir);
    res.status(200).json({ success: true, court, totalCount: files.length, files });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const downloadJudgment = (req: Request, res: Response) => {
  try {
    const { court, filename } = req.params;
    const dirs: Record<string, string> = {
      "supreme-court": uploadDirs.supremeCourt,
      "high-court": uploadDirs.highCourt,
      tribunal: uploadDirs.tribunal,
    };
    const filePath = path.join(dirs[court], filename);
    if (!fs.existsSync(filePath)) return res.status(404).json({ success: false, message: "File not found" });
    res.download(filePath);
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};

export const getUploadStats = (req: Request, res: Response) => {
  try {
    const stats: Record<string, any> = {};
    for (const [courtName, courtDir] of Object.entries(uploadDirs)) {
      const files = fs.readdirSync(courtDir);
      const totalSize = files.reduce((sum, file) => sum + fs.statSync(path.join(courtDir, file)).size, 0);
      stats[courtName] = { fileCount: files.length, totalSizeMB: (totalSize / (1024 * 1024)).toFixed(2) };
    }
    res.status(200).json({ success: true, stats });
  } catch (error: any) {
    res.status(500).json({ success: false, message: error.message });
  }
};
