import Draft from "../models/draft.model";

// ============================================
// 🔥 SAVE (WITH VERSIONING)
// ============================================

export const saveFinalDraft = async (data: any, userId: string) => {
  const latest = await Draft.findOne({ caseId: data.caseId })
    .sort({ version: -1 });

  const version = latest ? latest.version + 1 : 1;

  const draft = await Draft.create({
    ...data,
    version,
    createdBy: userId,
    isFinal: true,
  });

  return draft;
};

// ============================================
// 🔥 GET BY CASE
// ============================================

export const getDraftsByCase = async (caseId: string) => {
  return Draft.find({ caseId }).sort({ version: -1 });
};

// ============================================
// 🔥 GET SINGLE
// ============================================

export const getDraftById = async (id: string) => {
  return Draft.findById(id);
};

// ============================================
// 🔥 UPDATE (CREATE NEW VERSION)
// ============================================

export const updateDraft = async (id: string, content: string) => {
  const old = await Draft.findById(id);

  if (!old) throw new Error("Draft not found");

  const newDraft = await Draft.create({
    ...old.toObject(),
    _id: undefined,
    content,
    version: old.version + 1,
    updatedAt: new Date(),
  });

  return newDraft;
};

// ============================================
// 🔥 DELETE
// ============================================

export const deleteDraft = async (id: string) => {
  return Draft.findByIdAndDelete(id);
};
