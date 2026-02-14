import path from "path";

export interface ParsedJudgmentPath {
  court: string;
  year: number;
  month: number;
  date: number;
}

export function validateJudgmentPath(filePath: string): ParsedJudgmentPath | null {
  const parts = path.normalize(filePath).split(path.sep);

  if (parts.length < 5) return null;

  // Always read from end
  const fileName = parts[parts.length - 1];
  const dateStr = parts[parts.length - 2];
  const monthStr = parts[parts.length - 3];
  const yearStr = parts[parts.length - 4];
  const court = parts[parts.length - 5];

  const year = Number(yearStr);
  const month = Number(monthStr);
  const date = Number(dateStr);

  if (!court) return null;
  if (isNaN(year) || year < 1900 || year > 2100) return null;
  if (isNaN(month) || month < 1 || month > 12) return null;
  if (isNaN(date) || date < 1 || date > 31) return null;

  return { court, year, month, date };
}
