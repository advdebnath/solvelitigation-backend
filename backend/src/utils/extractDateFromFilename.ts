export function extractDateFromFilename(filename: string) {
  // Patterns:
  // 20250501
  // 01-05-2025
  // 01_05_2025
  const ymd = filename.match(/(20\d{2})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])/);
  if (ymd) {
    return {
      year: Number(ymd[1]),
      month: Number(ymd[2]),
      date: Number(ymd[3]),
    };
  }

  const dmy = filename.match(/(0[1-9]|[12]\d|3[01])[-_](0[1-9]|1[0-2])[-_](20\d{2})/);
  if (dmy) {
    return {
      year: Number(dmy[3]),
      month: Number(dmy[2]),
      date: Number(dmy[1]),
    };
  }

  return null; // fallback later
}
