import PDFDocument from "pdfkit";
import fs from "fs";
import path from "path";

// ============================================
// 📄 COURT-STYLE PDF GENERATOR (UPGRADED)
// ============================================

export const generatePetitionPDF = (text: string): string => {
  const filePath = path.join(
    "/tmp",
    `petition_${Date.now()}.pdf`
  );

  const doc = new PDFDocument({
    size: "A4",
    margins: {
      top: 100,
      bottom: 80,
      left: 80,
      right: 60,
    },
  });

  doc.pipe(fs.createWriteStream(filePath));

  // =========================================
  // 🏛️ HEADER (CENTERED)
  // =========================================

  doc
    .font("Times-Bold")
    .fontSize(14)
    .text("IN THE HON’BLE COURT", {
      align: "center",
    });

  doc.moveDown(1);

  // =========================================
  // 📄 BODY
  // =========================================

  const lines = text.split("\n");

  lines.forEach((line) => {
    const cleanLine = line.trim();

    // 🔥 Section Titles
    if (
      cleanLine.toUpperCase().includes("FACTS") ||
      cleanLine.toUpperCase().includes("GROUNDS") ||
      cleanLine.toUpperCase().includes("PRAYER") ||
      cleanLine.toUpperCase().includes("ISSUE")
    ) {
      doc.moveDown(1);
      doc
        .font("Times-Bold")
        .fontSize(12)
        .text(cleanLine, { align: "left" });
      doc.moveDown(0.5);
    } else {
      doc
        .font("Times-Roman")
        .fontSize(11)
        .text(cleanLine, {
          align: "justify",
          lineGap: 2,
        });
    }
  });

  // =========================================
  // 📌 FOOTER (PAGE NUMBER)
  // =========================================

  const range = doc.bufferedPageRange();

  for (let i = 0; i < range.count; i++) {
    doc.switchToPage(i);

    doc
      .fontSize(9)
      .text(
        `Page ${i + 1}`,
        0,
        doc.page.height - 50,
        {
          align: "center",
        }
      );
  }

  doc.end();

  return filePath;
};
