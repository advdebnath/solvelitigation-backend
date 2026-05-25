import PDFDocument from "pdfkit";
import fs from "fs";
import path from "path";

// ============================================
// 📄 GENERATE PDF
// ============================================

export const generatePDF = (report: any): string => {
  const filePath = path.join(
    "/tmp",
    `legal_report_${Date.now()}.pdf`
  );

  const doc = new PDFDocument();
  doc.pipe(fs.createWriteStream(filePath));

  doc.fontSize(18).text("LEGAL RESEARCH REPORT", { align: "center" });

  doc.moveDown();

  doc.fontSize(12).text(`Query: ${report.query}`);

  doc.moveDown();
  doc.text(`Issue:\n${report.issue}`);

  doc.moveDown();
  doc.text(`Rule:\n${report.rule}`);

  doc.moveDown();
  doc.text(`Application:\n${report.application}`);

  doc.moveDown();
  doc.text(`Conclusion:\n${report.conclusion}`);

  doc.moveDown();
  doc.text("Reasoning:");

  report.reasoning?.reasoning?.forEach((r: string) => {
    doc.text(`- ${r}`);
  });

  doc.moveDown();
  doc.text("Citations:");

  report.citations?.forEach((c: any) => {
    doc.text(`- ${c.case} (${c.citation}) [Score: ${c.score}]`);
  });

  doc.end();

  return filePath;
};
