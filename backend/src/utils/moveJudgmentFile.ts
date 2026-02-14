import fs from "fs";
import path from "path";

export function moveJudgmentFile(
  src: string,
  target: "processed" | "failed"
) {
  const dest = src.replace(
    "/data/judgments/inbox",
    `/data/judgments/${target}`
  );

  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.renameSync(src, dest);

  return dest;
}
