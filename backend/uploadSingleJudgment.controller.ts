export const uploadSingleJudgment = async (req: Request, res: Response) => {
  try {
    const user = req.currentUser;
    if (!user) return res.status(401).json({ message: "Unauthorized" });
    if (!req.file) return res.status(400).json({ message: "No file uploaded" });

    const title =
      req.body?.title?.trim() ||
      req.file.originalname.replace(/\.pdf$/i, "");

    const judgment = await Judgment.create({
      title,
      courtType: req.body.courtType, // SUPREME_COURT | HIGH_COURT | TRIBUNAL
      category: "UNCLASSIFIED",
      year: Number(req.body.year) || new Date().getFullYear(),
      uploadedBy: user._id,
      file: {
        originalname: req.file.originalname,
        filename: req.file.filename,
        path: req.file.path,
        size: req.file.size,
        mimetype: req.file.mimetype,
      },
      nlpStatus: "PENDING",
    });

    return res.status(201).json({
      success: true,
      judgmentId: judgment._id,
    });
  } catch (err) {
    console.error(err);
    res.status(500).json({ message: "Upload failed" });
  }
};
