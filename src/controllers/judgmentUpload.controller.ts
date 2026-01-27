import { Request, Response } from "express";

export const uploadSingleJudgment = async (req: Request, res: Response) => {
  try {
    if (!req.file) {
      return res.status(400).json({
        success: false,
        message: "No PDF file uploaded",
      });
    }

    const { court, year, category } = req.body;

    return res.json({
      success: true,
      message: "Judgment uploaded successfully",
      file: {
        originalName: req.file.originalname,
        storedName: req.file.filename,
        path: req.file.path, // /tmp/xxxx.pdf
        size: req.file.size,
      },
      meta: {
        court,
        year,
        category,
      },
    });
  } catch (error) {
    console.error("UPLOAD ERROR:", error);
    return res.status(500).json({
      success: false,
      message: "Judgment upload failed",
    });
  }
};
