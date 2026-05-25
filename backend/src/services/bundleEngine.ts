import fs from "fs";
import path from "path";
import PDFDocument from "pdfkit";

import { generatePetition, generateAffidavit, generateVakalatnama } from "./petitionEngine";

// ============================================
// 📄 WRITE SECTION + COUNT PAGES
// ============================================

const writeSection = (doc: PDFKit.PDFDocument, title: string, text: string) => {
  const startPage = doc.bufferedPageRange().count + 1;

  doc.addPage();

  doc.font("Times-Bold").fontSize(14).text(title, { align: "center" });
  doc.moveDown();

  doc.font("Times-Roman").fontSize(11).text(text, {
    align: "justify",
    lineGap: 2,
  });

  const endPage = doc.bufferedPageRange().count;

  return { startPage, endPage };
};

// ============================================
// 📑 BUILD INDEX (REAL)
// ============================================

const buildIndexPage = (doc: PDFKit.PDFDocument, indexData: any[]) => {
  doc.switchToPage(0);

  doc.font("Times-Bold").fontSize(14).text("INDEX", { align: "center" });
  doc.moveDown();

  doc.font("Times-Roman").fontSize(11);

  indexData.forEach((item, i) => {
    doc.text(`${i + 1}. ${item.title} .......... Page ${item.page}`);
  });
};

// ============================================
// 📄 MAIN GENERATOR (FINAL FIXED)
// ============================================

export const generateBundlePDF = async ({
  type,
  facts,
  query,
  name,
  client,
  advocate,
  annexures = [],
}: any) => {
  const filePath = path.join("/tmp", `bundle_${Date.now()}.pdf`);

  const doc = new PDFDocument({
    size: "A4",
    margins: { top: 80, bottom: 60, left: 70, right: 50 },
    bufferPages: true,
  });

  doc.pipe(fs.createWriteStream(filePath));

  // =========================================
  // PLACEHOLDER INDEX PAGE
  // =========================================
  doc.addPage();

  // =========================================
  // GENERATE CONTENT
  // =========================================

  // 🔥 FIX: TYPE-SAFE PETITION
  const petitionResult = await generatePetition({
    type,
    facts,
    query,
    annexures,
  });

  if (!petitionResult || typeof petitionResult !== "string") {
    throw new Error("Petition generation failed");
  }

  const petition = petitionResult;

  const affidavit = generateAffidavit(name, facts);
  const vakalatnama = generateVakalatnama(client, advocate);

  const indexData: any[] = [];

  // PETITION
  const p = writeSection(doc, "PETITION", petition);
  indexData.push({ title: "Petition", page: p.startPage });

  // AFFIDAVIT
  const a = writeSection(doc, "AFFIDAVIT", affidavit);
  indexData.push({ title: "Affidavit", page: a.startPage });

  // VAKALATNAMA
  const v = writeSection(doc, "VAKALATNAMA", vakalatnama);
  indexData.push({ title: "Vakalatnama", page: v.startPage });

  // ANNEXURES
  if (annexures.length) {
    const annexText = annexures
      .map((a: string, i: number) => `ANNEXURE A${i + 1}\n\n${a}`)
      .join("\n\n");

    const an = writeSection(doc, "ANNEXURES", annexText);
    indexData.push({ title: "Annexures", page: an.startPage });
  }

  // =========================================
  // BUILD INDEX PAGE
  // =========================================

  buildIndexPage(doc, indexData);

  // =========================================
  // ADD PAGE NUMBERS
  // =========================================

  const range = doc.bufferedPageRange();

  for (let i = 0; i < range.count; i++) {
    doc.switchToPage(i);

    doc.fontSize(9).text(
      `Page ${i + 1}`,
      0,
      doc.page.height - 50,
      { align: "center" }
    );
  }

  doc.end();

  return filePath;
};
