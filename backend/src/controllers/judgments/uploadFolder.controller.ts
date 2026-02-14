import { Request, Response } from "express";
import axios from "axios";
import { Judgment } from "../../models";

/**
 * POST /api/judgments/upload-folder
 * ADMIN / SUPERADMIN
 * Upload multiple PDFs → auto NLP enqueue
 */
export const uploadFolder = async (req: Request, res: Response) => {
  try {
    const user = req.currentUser || req.user;

    if (!user) {
      return res.status(401).json({ message: "Not authenticated" });
    }

    const files = req.files as Express.Multer.File[];

    if (!files || files.length === 0) {
      return res.status(400).json({ message: "No files uploaded" });
    }

    const created: any[] = [];

    for (const file of files) {
      const judgment = await Judgment.create({
        title: file.originalname.replace(/\.pdf$/i, ""),
        year: new Date().getFullYear(),
        courtType: "UNKNOWN",
        category: "UNCLASSIFIED",
        uploadedBy: user._id.toString(),
        uploadedAt: new Date(),
        nlpStatus: "PENDING",
        nlp: { status: "PENDING" },
        file: {
          originalname: file.originalname,
          filename: file.filename,
          path: file.path,
          size: file.size,
          mimetype: file.mimetype,
        },
      });

      // enqueue NLP (non-blocking)
      axios
        .post("http://127.0.0.1:4000/api/nlp/enqueue", {
          judgmentId: judgment._id.toString(),
        })
        .catch(() => {});

      created.push(judgment._id);
    }

    return res.status(201).json({
      success: true,
      count: created.length,
      judgmentIds: created,
    });
  } catch (error) {
    console.error("❌ uploadFolder failed:", error);
    return res.status(500).json({
      message: "Folder upload failed",
    });
  }
};
