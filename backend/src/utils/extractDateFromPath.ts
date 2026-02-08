export function extractDateFromPath(filePath: string) {
  const parts = filePath.split("/").filter(Boolean);

  const day = Number(parts.at(-2));
  const month = Number(parts.at(-3));
  const year = Number(parts.at(-4));

  if (
    year >= 1900 &&
    month >= 1 && month <= 12 &&
    day >= 1 && day <= 31
  ) {
    return { year, month, day };
  }

  return null;
}
