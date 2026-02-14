import fs from "fs";
import path from "path";
import * as cheerio from "cheerio";

const SOURCE_ROOT = "/data/judgments/judgment";
const TARGET_ROOT = "/data/judgments/normalized";

/**
 * Remove header garbage but keep:
 * ✔ footnotes
 * ✔ page numbers
 * ✔ images
 */
function normalizeHtmlFile(inputFile: string, outputFile: string) {
  const html = fs.readFileSync(inputFile, "utf8");
  const $ = cheerio.load(html);

  /** 🔥 Remove obvious header junk */
  $("title").remove();
  $("meta[name='generator']").remove();

  /** 🔥 Remove footer garbage (pattern-based, SAFE) */
  $("body")
    .find("*")
    .each((_, el) => {
      const text = $(el).text().toLowerCase();

      if (
        text.match(
          /downloaded from|printed on|digitally signed|signature not verified|computer generated|www\./
        )
      ) {
        $(el).remove();
      }
    });

  /** ✅ Preserve images, layout, footnotes */
  fs.mkdirSync(path.dirname(outputFile), { recursive: true });
  fs.writeFileSync(outputFile, $.html(), "utf8");
}

/**
 * Recursively normalize all HTML files
 */
function walk(dir: string) {
  for (const entry of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, entry);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      walk(fullPath);
      continue;
    }

    if (!entry.endsWith(".html")) continue;

    const relative = path.relative(SOURCE_ROOT, fullPath);
    const target = path.join(TARGET_ROOT, relative);

    console.log(`🧹 Normalizing: ${fullPath}`);
    normalizeHtmlFile(fullPath, target);
  }
}

console.log("🧹 HTML normalization started");
walk(SOURCE_ROOT);
console.log("✅ HTML normalization completed");
