export type DocumentType =
  | "JUDGMENT"
  | "CAUSE_LIST"
  | "NOTIFICATION"
  | "CIRCULAR"
  | "ACT"
  | "RULE";

export type ProcessingMode =
  | "FULL_NLP"
  | "STORE_ONLY";

export interface ClassificationResult {
  documentType: DocumentType;
  processingMode: ProcessingMode;
  confidence: number;
}

export function classifyDocument(
  text: string
): ClassificationResult {

  const content =
    (text || "").toUpperCase();

  // =====================================
  // CAUSE LISTS
  // =====================================

  if (
    content.includes("CAUSE LIST") ||
    content.includes("DAILY LIST") ||
    content.includes("SUPPLEMENTARY LIST") ||
    content.includes("ADVANCE LIST") ||
    content.includes("ORAL MENTIONING") ||
    content.includes("LIST OF MATTERS") ||
    content.includes("COURT NO.") ||
    content.includes("ITEM NO.")
  ) {
    return {
      documentType: "CAUSE_LIST",
      processingMode: "STORE_ONLY",
      confidence: 95,
    };
  }

  // =====================================
  // NOTIFICATIONS
  // =====================================

  if (
    content.includes("NOTIFICATION") ||
    content.includes("PUBLIC NOTICE") ||
    content.includes("GAZETTE")
  ) {
    return {
      documentType: "NOTIFICATION",
      processingMode: "STORE_ONLY",
      confidence: 90,
    };
  }

  // =====================================
  // CIRCULARS
  // =====================================

  if (
    content.includes("CIRCULAR") ||
    content.includes("OFFICE ORDER")
  ) {
    return {
      documentType: "CIRCULAR",
      processingMode: "STORE_ONLY",
      confidence: 90,
    };
  }

  // =====================================
  // ACTS
  // =====================================

  if (
    content.includes("AN ACT") &&
    content.includes("BE IT ENACTED")
  ) {
    return {
      documentType: "ACT",
      processingMode: "STORE_ONLY",
      confidence: 95,
    };
  }

  // =====================================
  // RULES
  // =====================================

  if (
    content.includes("RULES") &&
    content.includes("IN EXERCISE OF THE POWERS")
  ) {
    return {
      documentType: "RULE",
      processingMode: "STORE_ONLY",
      confidence: 95,
    };
  }

  // =====================================
  // DEFAULT
  // =====================================

  return {
    documentType: "JUDGMENT",
    processingMode: "FULL_NLP",
    confidence: 80,
  };
}
