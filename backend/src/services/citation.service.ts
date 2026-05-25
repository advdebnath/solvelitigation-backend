export const buildCitationArgument = (
  argument: string,
  cases: any[]
) => {
  if (!argument) return "";

  if (!cases || cases.length === 0) {
    return argument;
  }

  const citations = cases
    .map((c: any) => c.caseNumber || c.id || "Case")
    .filter(Boolean)
    .join(", ");

  return `
${argument}

SUPPORTED BY:

The above legal position is supported by judicial precedents including ${citations}.
`.trim();
};
