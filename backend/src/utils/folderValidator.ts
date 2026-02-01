import path from "path";

export interface FolderMeta {
  year: number;
  month: number;
  day: number;
}

/**
 * Validates strict YYYY/MM/DD folder structure for judgment PDFs
 * Expected relative path: YYYY/MM/DD/file.pdf
 */
export function validateJudgmentPath(
  basePath: string,
  filePath: string
): FolderMeta {
  const relative = path.relative(basePath, filePath);
  const parts = relative.split(path.sep);

  // Expect at least: YYYY/MM/DD/file.pdf
  if (parts.length < 4) {
    throw new Error("Invalid folder depth: expected YYYY/MM/DD/file.pdf");
  }

  const [yearStr, monthStr, dayStr] = parts;

  // Year: YYYY
  const year = Number(yearStr);
  if (!/^\d{4}$/.test(yearStr) || year < 1900 || year > 2100) {
    throw new Error(`Invalid year folder: ${yearStr}`);
  }

  // Month: MM (01–12)
  const month = Number(monthStr);
  if (!/^\d{2}$/.test(monthStr) || month < 1 || month > 12) {
    throw new Error(`Invalid month folder: ${monthStr}`);
  }

  // Day: DD (calendar-safe)
  const day = Number(dayStr);
  const maxDays = new Date(year, month, 0).getDate();
  if (!/^\d{2}$/.test(dayStr) || day < 1 || day > maxDays) {
    throw new Error(`Invalid date folder: ${dayStr}`);
  }

  return { year, month, day };
}
