import path from "path";

export interface ParsedJudgmentPath {
  court: string;
  year: number;
  month: number;
  date: number;
}

export function validateJudgmentPath(filePath: string): ParsedJudgmentPath | null {
  const parts = path.normalize(filePath).split(path.sep);

  // expect: /data/judgments/inbox/<court>/<year>/<month>/<date>/<file>.pdf
  const len = parts.length;
  if (len < 6) return null;

  const court = parts[len - 5];
  const year = Number(parts[len - 4]);
  const month = Number(parts[len - 3]);
  const date = Number(parts[len - 2]);

  if (!court) return null;
  if (year < 1900 || year > 2100) return null;
  if (month < 1 || month > 12) return null;
  if (date < 1 || date > 31) return null;

  return { court, year, month, date };
}

