import JudgmentIngestion from "../models/JudgmentIngestion";
import { exec } from "child_process";
import fs from "fs";
import path from "path";

/**
 * 🔥 Convert PDF → HTML (PERMANENT FIX)
 */
const convertPdfToHtml = (pdfPath: string): Promise<void> => {
  return new Promise((resolve, reject) => {
    const htmlPath = pdfPath.replace(".pdf", ".html");

    // ✅ Skip if already converted
    if (fs.existsSync(htmlPath)) {
      console.log("✅ HTML already exists:", htmlPath);
      return resolve();
    }

    const cmd = `pdftohtml -enc UTF-8 -noframes "${pdfPath}" "${htmlPath}"`;

    console.log("⚙️ Converting PDF → HTML:", pdfPath);

    exec(cmd, (err) => {
      if (err) {
        console.error("❌ HTML conversion failed:", err);
        return reject(err);
      }

      console.log("✅ HTML created:", htmlPath);
      resolve();
    });
  });
};

/**
 * 🚀 Move ingestions from UPLOADED → QUEUED
 * 🔥 ALSO ensures HTML is created before NLP
 */
export async function enqueueIngestions(ingestionIds: string[]) {
  if (!ingestionIds.length) return;

  // 🔥 Fetch ingestions first (to access file paths)
  const ingestions = await JudgmentIngestion.find({
    _id: { $in: ingestionIds },
    status: "UPLOADED",
  });

  for (const ingestion of ingestions) {
    try {
      const relativePath = ingestion.file?.relativePath;

      if (!relativePath) {
        console.warn("⚠️ Missing file path for ingestion:", ingestion._id);
        continue;
      }

      // 🔥 Build absolute path
      const absolutePath = path.join(
        "/var/www/solvelitigation/backend",
        relativePath
      );

      // 🔥 Convert PDF → HTML BEFORE QUEUE
      try {
        await convertPdfToHtml(absolutePath);
      } catch (err) {
        console.error(
          "⚠️ HTML conversion failed for:",
          ingestion._id,
          err
        );
      }

    } catch (err) {
      console.error("❌ Error preparing ingestion:", ingestion._id, err);
    }
  }

  // 🔥 Finally move to QUEUED
  await JudgmentIngestion.updateMany(
    {
      _id: { $in: ingestionIds },
      status: "UPLOADED",
    },
    {
      $set: {
        status: "QUEUED",
        queuedAt: new Date(),
      },
    }
  );

  console.log(`🚀 Enqueued ${ingestionIds.length} ingestion(s)`);
}
