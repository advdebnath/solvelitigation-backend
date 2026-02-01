import fs from "fs";
import path from "path";
import crypto from "crypto";

const INBOX = process.env.INBOX_ROOT || "/data/judgments/inbox";

function hashFile(filePath: string): Promise<string> {
  return new Promise((resolve, reject) => {
    const hash = crypto.createHash("sha256");
    const stream = fs.createReadStream(filePath);
    stream.on("data", d => hash.update(d));
    stream.on("end", () => resolve(hash.digest("hex")));
    stream.on("error", reject);
  });
}

function walk(dir: string, files: string[] = []) {
  for (const f of fs.readdirSync(dir)) {
    const p = path.join(dir, f);
    const st = fs.statSync(p);
    if (st.isDirectory()) walk(p, files);
    else if (p.toLowerCase().endsWith(".pdf")) files.push(p);
  }
  return files;
}

export const dryRunScan = async (_req: any, res: any) => {
  const pdfs = walk(INBOX);
  const seen = new Set<string>();
  const dups: string[] = [];
  const bad: string[] = [];

  for (const p of pdfs) {
    try {
      const h = await hashFile(p);
      if (seen.has(h)) dups.push(p);
      else seen.add(h);
    } catch {
      bad.push(p);
    }
  }

  return res.json({
    mode: "scan_only",
    inbox: INBOX,
    totalFound: pdfs.length,
    unique: seen.size,
    duplicates: dups.length,
    corrupt: bad.length
  });
};
