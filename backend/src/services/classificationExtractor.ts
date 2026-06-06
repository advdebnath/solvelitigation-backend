import fs from "fs";
import path from "path";
import { execSync } from "child_process";

export function extractClassificationText(
  pdfPath: string
): string {

  try {

    const txtFile =
      path.join(
        "/tmp",
        `classification_${Date.now()}.txt`
      );

    execSync(
      `pdftotext -f 1 -l 2 "${pdfPath}" "${txtFile}"`,
      {
        stdio: "ignore"
      }
    );

    if (!fs.existsSync(txtFile)) {
      return "";
    }

    const text =
      fs.readFileSync(
        txtFile,
        "utf8"
      );

    fs.unlinkSync(txtFile);

    return text || "";

  } catch (err) {

    console.error(
      "❌ Classification extraction failed:",
      err
    );

    return "";
  }
}
