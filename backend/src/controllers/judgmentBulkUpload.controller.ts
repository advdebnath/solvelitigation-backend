import fs from "fs";
import path from "path";
import { Request, Response } from "express";
import { uploadSingleJudgment } from "./judgmentUpload.controller";

export const uploadBulkJudgments = async (req: Request, res: Response) => {
  try {
    const { folderPath, courtType, category } = req.body;

    if (!folderPath || !courtType || !category) {
      return res.status(400).json({
        success: false,
        message: "folderPath, courtType, category are required",
      });
    }

    if (!fs.existsSync(folderPath)) {
      return res.status(400).json({
        success: false,
        message: "Folder path does not exist",
      });
    }

    const results: any[] = [];

    const walk = async (dir: string) => {
      const entries = fs.readdirSync(dir, { withFileTypes: true });

      for (const entry of entries) {
        const fullPath = path.join(dir, entry.name);

        if (entry.isDirectory()) {
          await walk(fullPath);
          continue;
        }

        if (!entry.name.toLowerCase().endsWith(".pdf")) continue;

        // Expecting .../YEAR/MONTH/DATE/file.pdf
        const parts = fullPath.split(path.sep);
        const date = parts[parts.length - 2];
        const month = parts[parts.length - 3];
        const year = parts[parts.length - 4];

        try {
          await uploadSingleJudgment(
            {
              ...req,
              file: {
                path: fullPath,
                originalname: entry.name,
              },
              body: {
                courtType,
                category,
                year,
                month,
                date,
              },
            } as any,
            {
              json: (data: any) =>
                results.push({ file: entry.name, ...data }),
              status: () => ({
                json: (data: any) =>
                  results.push({ file: entry.name, ...data }),
              }),
            } as any
          );
        } catch (err: any) {
          results.push({
            file: entry.name,
            success: false,
            error: err.message,
          });
        }
      }
    };

    await walk(folderPath);

    return res.json({
      success: true,
      total: results.length,
      results,
    });
  } catch (err: any) {
    return res.status(500).json({
      success: false,
      message: err.message,
    });
  }
};
