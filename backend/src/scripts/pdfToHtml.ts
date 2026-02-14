import fs from "fs";
import path from "path";
import { execSync } from "child_process";

/**
 * CONFIG
 */
const ROOT = "/data/judgments/judgment"; // 🔐 ONLY this root
const ALLOWED_COURTS = ["supreme-court", "high-court", "tribunal"];

/**
 * Entry
 */
(function run() {
  console.log("📄 PDF → HTML batch started");
  walk(ROOT);
  console.log("✅ PDF → HTML batch completed");
})();

/**
 * Recursive walker
 */
function walk(dir: string) {
  if (!fs.existsSync(dir)) return;

  const entries = fs.readdirSync(dir);

  for (const entry of entries) {
    const fullPath = path.join(dir, entry);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      validateFolder(fullPath);
      walk(fullPath);
      continue;
    }

    if (!entry.toLowerCase().endsWith(".pdf")) continue;

    convertPdf(fullPath);
  }
}

/**
 * Folder validation (audit safety)
 */
function validateFolder(folderPath: string) {
  const parts = folderPath.split(path.sep);
  const idx = parts.indexOf("judgment");

  if (idx === -1) return;

  const court = parts[idx + 1];
  const decade = parts[idx + 2];

  if (court && !ALLOWED_COURTS.includes(court)) {
    throw new Error(`❌ Invalid court folder: ${court}`);
  }

  if (decade && !/^\d{4}-\d{4}$/.test(decade)) {
    throw new Error(`❌ Invalid decade block: ${decade}`);
  }
}

/**
 * PDF → HTML conversion
 */
function convertPdf(pdfPath: string) {
  const htmlPath = pdfPath.replace(/\.pdf$/i, ".html");

  // ⏭️ Skip if already converted
  if (fs.existsSync(htmlPath)) {
    return;
  }

  console.log(`➡️ Converting: ${pdfPath}`);

  try {
    execSync(
      `pdftohtml -c -hidden -noframes -s "${pdfPath}" "${htmlPath}"`,
      { stdio: "ignore" }
    );
  } catch (err) {
    console.error(`❌ Failed: ${pdfPath}`);
  }
}
