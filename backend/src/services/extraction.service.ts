import fs from "fs";
import path from "path";
import { execSync } from "child_process";

const safeExec = (cmd: string) => {
  try {
    execSync(cmd, { stdio: "ignore" });
    return true;
  } catch {
    return false;
  }
};

const cleanText = (text: string) => {
  return text
    .replace(/[^a-zA-Z0-9\s.,:;()\-\/]/g, " ")
    .replace(/\s+/g, " ")
    .trim();
};

export const extractTextFromFile = (filePath: string): string => {
  const ext = path.extname(filePath).toLowerCase();

  let text = "";

  try {
    // ============================================
    // 🔥 TXT
    // ============================================
    if (ext === ".txt") {
      return cleanText(fs.readFileSync(filePath, "utf-8"));
    }

    // ============================================
    // 🔥 PDF → IMAGES → OCR (PERMANENT FIX)
    // ============================================
    if (ext === ".pdf") {
      const base = filePath.replace(".pdf", "");
      const imgPrefix = base + "_page";

      // 1️⃣ Convert PDF → images
      const pdfToImg = safeExec(
        `pdftoppm -png "${filePath}" "${imgPrefix}"`
      );

      if (!pdfToImg) return "";

      // 2️⃣ OCR each image
      const dir = path.dirname(filePath);
      const files = fs.readdirSync(dir);

      let combined = "";

      for (const f of files) {
        if (f.startsWith(path.basename(imgPrefix)) && f.endsWith(".png")) {
          const imgPath = path.join(dir, f);
          const outBase = imgPath.replace(".png", "");

          const ocrOk = safeExec(`tesseract "${imgPath}" "${outBase}"`);

          if (ocrOk) {
            const txtFile = outBase + ".txt";
            if (fs.existsSync(txtFile)) {
              combined += fs.readFileSync(txtFile, "utf-8") + " ";
              fs.unlinkSync(txtFile);
            }
          }

          fs.unlinkSync(imgPath);
        }
      }

      text = combined;
    }

  } catch (err) {
    console.error("❌ Extraction service error:", err);
  }

  return cleanText(text);
};
