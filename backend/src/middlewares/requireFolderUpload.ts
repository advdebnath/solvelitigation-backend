import { Request, Response, NextFunction } from "express";

export const requireFolderUpload = (
  req: Request,
  res: Response,
  next: NextFunction
) => {
  const files = req.files as Express.Multer.File[];

  if (!files || files.length === 0) {
    return res.status(400).json({
      message: "Folder upload required",
    });
  }

  const isFolderUpload = files.some((f) => {
    const relativePath = (f as any).webkitRelativePath;
    return (
      typeof relativePath === "string" &&
      /\/\d{4}\/\d{2}\/\d{2}\//.test(relativePath)
    );
  });

  if (!isFolderUpload) {
    return res.status(400).json({
      message:
        "Single PDF upload is disabled. Upload YEAR/MONTH/DATE folder only.",
    });
  }

  next();
};
