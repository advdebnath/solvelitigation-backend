import Volume from "../models/volume.model";

export const generateSLSC = async (year: number, pageCount: number) => {
  let volumeDoc = await Volume.findOne({ year }).sort({ volume: -1 });

  // 🔥 FIRST ENTRY
  if (!volumeDoc) {
    volumeDoc = await Volume.create({
      year,
      volume: 1,
      currentPage: 1,
    });
  }

  // 🔥 CHECK OVERFLOW
  if (volumeDoc.currentPage + pageCount > 900) {
    volumeDoc = await Volume.create({
      year,
      volume: volumeDoc.volume + 1,
      currentPage: 1,
    });
  }

  const startPage = volumeDoc.currentPage;
  const endPage = startPage + pageCount - 1;

  // 🔥 UPDATE PAGE
  volumeDoc.currentPage = endPage + 1;
  await volumeDoc.save();

  const slscCitation = `${year} (${volumeDoc.volume}) SLSC ${startPage}`;

  return {
    slscCitation,
    startPage,
    endPage,
    pageCount,
  };
};
