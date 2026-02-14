import fs from "fs";
import path from "path";
import * as cheerio from "cheerio";

const INPUT_ROOT = "/data/judgments/normalized";
const OUTPUT_ROOT = "/data/judgments/enriched";

const JUDGMENT_REGEX =
  /(J\s*U\s*D\s*G\s*M\s*E\s*N\s*T|O\s*R\s*D\s*E\s*R|JUDGMENT|ORDER)/i;

const COST_REGEX =
  /(COSTS?|Costs?|Costs awarded)/i;

function ensureDir(dir: string) {
  if (!fs.existsSync(dir)) {
    fs.mkdirSync(dir, { recursive: true });
  }
}

function walk(dir: string, callback: (file: string) => void) {
  for (const entry of fs.readdirSync(dir)) {
    const fullPath = path.join(dir, entry);
    const stat = fs.statSync(fullPath);

    if (stat.isDirectory()) {
      walk(fullPath, callback);
    } else if (entry.endsWith(".html")) {
      callback(fullPath);
    }
  }
}

function insertHeadnote(htmlPath: string) {
  const html = fs.readFileSync(htmlPath, "utf-8");
  const $ = cheerio.load(html, { decodeEntities: false });

  const body = $("body");
  if (!body.length) return;

  let judgmentNode: cheerio.Element | null = null;
  let costNode: cheerio.Element | null = null;

  body.find("*").each((_, el) => {
    const text = $(el).text().trim();

    if (!judgmentNode && JUDGMENT_REGEX.test(text)) {
      judgmentNode = el;
    }

    if (!costNode && COST_REGEX.test(text)) {
      costNode = el;
    }
  });

  if (!judgmentNode) {
    console.warn("⚠️ No JUDGMENT/ORDER found:", htmlPath);
    return;
  }

  const headnoteBlock = `
    <div class="headnote-block" style="border:1px solid #000; padding:12px; margin:16px 0;">
      <h2 style="text-align:center;">HEADNOTE</h2>
      <p><!-- NLP HEADNOTE WILL BE INSERTED HERE --></p>
    </div>
  `;

  if (costNode) {
    $(costNode).after(headnoteBlock);
  } else {
    $(judgmentNode).before(headnoteBlock);
  }

  const relative = path.relative(INPUT_ROOT, htmlPath);
  const outPath = path.join(OUTPUT_ROOT, relative);

  ensureDir(path.dirname(outPath));
  fs.writeFileSync(outPath, $.html(), "utf-8");

  console.log("📝 Headnote inserted:", outPath);
}

console.log("🧠 Step 4: Headnote insertion started");

ensureDir(OUTPUT_ROOT);

walk(INPUT_ROOT, insertHeadnote);

console.log("✅ Step 4 completed");
