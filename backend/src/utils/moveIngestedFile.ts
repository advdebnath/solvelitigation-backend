import fs from "fs";
import path from "path";

export function moveIngestedFile(
  src: string,
  base: "processed" | "failed"
) {
  const dest = src.replace(
    "/data/judgments/inbox",
    `/data/judgments/${base}`
  );

  fs.mkdirSync(path.dirname(dest), { recursive: true });
  fs.renameSync(src, dest);

  return dest;
}
