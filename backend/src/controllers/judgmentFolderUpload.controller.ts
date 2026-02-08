import fs from "fs";
import path from "path";
import { Request, Response } from "express";
import Judgment from "../models/Judgment";

/**
 * POST /api/judgments/upload-folder
 * Accepts ONLY a folder named `judgment`
 *
 * Expected structure:
 * judgment/
 *   supreme-court/
 *     1950-1960/
 *       1955/
 *         06/
 *           21/
 *             file.pdf
 */
export const uploadJudgmentFolder = async (req: Request, res: Response) => {
  try {
    const authUser = req.currentUser || req.user;
    if (!authUser) {
      return res.status(401).json({ message: "Not authenticated" });
    }
    const userId = authUser._id;

    const rootPath = req.body?.rootPath;
    if (!rootPath || !rootPath.endsWith(`${path.sep}judgment`)) {
      return res.status(400).json({
        message: "Only root folder named 'judgment' is allowed",
      });
    }

    if (!fs.existsSync(rootPath)) {
      return res.status(400).json({ message: "Folder not found on server" });
    }

    const inserted: string[] = [];
    const rejected: Array<{ file: string; error: string }> = [];

    walk(rootPath);

    function walk(currentPath: string) {
      const entries = fs.readdirSync(currentPath);

      for (const entry of entries) {
        const fullPath = path.join(currentPath, entry);
        const stat = fs.statSync(fullPath);

        if (stat.isDirectory()) {
          walk(fullPath);
          continue;
        }

        if (!entry.toLowerCase().endsWith(".pdf")) {
          continue;
        }

        try {
          const meta = parsePath(fullPath);

          const title =
            entry.replace(/\.pdf$/i, "").trim() || "Untitled Judgment";

          const judgment = new Judgment({
            title,
            courtType: meta.courtType,
            courtSubType: meta.courtSubType,
            decadeBlock: meta.decadeBlock,
            year: meta.year,
            month: meta.month,
            date: meta.date,
            sourcePath: fullPath,
            uploadedBy: userId,
            uploadedAt: new Date(),
            nlpStatus: "PENDING",
          });

          judgment.validateSync(); // 🔐 strict schema enforcement
          judgment.save(); // async-safe (mongoose queues internally)

          inserted.push(fullPath);
        } catch (err: any) {
          rejected.push({
            file: fullPath,
            error: err.message || "Unknown error",
          });
        }
      }
    }

    return res.json({
      success: true,
      inserted: inserted.length,
      rejected: rejected.length,
      rejectedFiles: rejected,
    });
  } catch (error) {
    console.error("❌ Folder upload failed:", error);
    return res.status(500).json({ message: "Folder upload failed" });
  }
};

/**
 * Parse metadata STRICTLY from folder structure
 */
function parsePath(filePath: string) {
  const parts = filePath.split(path.sep);
  const idx = parts.lastIndexOf("judgment");

  if (idx === -1) throw new Error("Invalid root folder");

  const court = parts[idx + 1];
  const decade = parts[idx + 2];
  const year = Number(parts[idx + 3]);
  const month = Number(parts[idx + 4]);
  const date = Number(parts[idx + 5]);

  if (!court || !decade || !year || !month || !date) {
    throw new Error("Invalid folder depth");
  }

  if (!/^\d{4}-\d{4}$/.test(decade)) {
    throw new Error("Invalid decade block");
  }

  if (month < 1 || month > 12) throw new Error("Invalid month");
  if (date < 1 || date > 31) throw new Error("Invalid date");

  return {
    courtType:
      court === "supreme-court"
        ? "SUPREME_COURT"
        : court === "high-court"
        ? "HIGH_COURT"
        : "TRIBUNAL",
    courtSubType: null,
    decadeBlock: decade,
    year,
    month,
    date,
  };
}
