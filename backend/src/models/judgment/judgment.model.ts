// backend/src/models/judgment.model.ts
import mongoose, { Document, Schema, Types, Model } from "mongoose";

/* ======================================================================== */
/* 🧩  Sub-Interfaces                                                        */
/* ======================================================================== */

export interface IParties {
  petitioner: string[];
  respondent: string[];
}

export interface IPointOfLaw {
  principle?: string;
  category?: string;
  actReference?: string;
  section?: string;
}

export interface ISectionRef {
  section: string;
  description?: string;
  linkedJudgments?: Types.ObjectId[];
}

export interface IActReference {
  actName: string;
  sections?: ISectionRef[];
  citations?: string[];
  actId?: Types.ObjectId;
}

export interface ICitation {
  caseName?: string;
  citationText?: string;
  citationType?:
    | "overruled"
    | "distinguished"
    | "followed"
    | "reversed"
    | "reliedOn"
    | "cited";
  citationReference?: string;
  judgmentId?: Types.ObjectId | string;
}

export interface IFileRef {
  filename: string;
  gridfsId: Types.ObjectId | string;
  fileId?: Types.ObjectId | string;
}

/* ======================================================================== */
/* 🧩 Main Interface (IJudgment)                                            */
/* ======================================================================== */

export interface IJudgment extends Document<Types.ObjectId> {

  nlpVersions?: {
    version: "original" | "reviewed";
    generatedAt: Date;
    generatedBy: "system" | "admin";
    jobId?: string;
    content: any;
  }[];

  htmlContent?: string;
  plainText?: string;
  summary?: string;
  headnotes?: string | string[];

  isAnalyzed?: boolean;
  nlpAnalysis?: {
    headnotes?: any;
    summary?: string;
    pointsOfLaw?: any[];
  };

  court?: string;
  courtLevel?: string; // e.g. "Supreme Court", "High Court", "Tribunal"
  courtName?: string;

  // ✅ canonical court type used by generateCaseNumber / uploads
  courtType?: "supreme" | "high" | "tribunal" | string;

  legalCategory?: "CIVIL" | "CRIMINAL" | "SERVICE" | "TAXATION" | "CORPORATE";
  category?: string;
  subCategory?: string;

  caseNumber?: string;
  judgmentDate?: Date;
  year?: number;
  month?: number;
  day?: number;
  judges?: string[];
  bench?: string;
  parties?: IParties;

  actReferences?: IActReference[];
  linkedActs?: Types.ObjectId[];
  legalPrinciples?: string[];
  pointsOfLaw?: IPointOfLaw[];

  citations?: ICitation[];
  files?: IFileRef[];

  storageType?: "gridfs" | "local";
  fileSize?: number;
  originalFilename?: string;
  originalName?: string;
  pdfPath?: string;

  fileId?: Types.ObjectId;
  sourceFile?: Types.ObjectId;

  /** uploader / owner links */
  uploadedBy?: Types.ObjectId;
  createdBy?: Types.ObjectId | string | null;

  /** pagination / volume info */
  volume?: number;
  startPage?: number;
  endingPage?: number; // ✅ ADDED (fixes TS2339)
  pages?: number;

  analysisStatus?: "pending" | "processing" | "completed" | "failed";
  analysisCompletedAt?: Date | null;

  summaryStatus?: "pending" | "processed" | "failed";
  summaryRetryCount?: number;

  reviewStatus?: "pending" | "approved" | "rejected";

  isReviewed?: boolean;
  reviewedBy?: string | null;
  reviewedAt?: Date | null;

  isAmended?: boolean;
  amendedBy?: string | null;
  amendedAt?: Date | null;

  isAuthorized?: boolean;
  authorizedBy?: string | null;
  authorizedAt?: Date | null;

  isOverruled?: boolean;
  isPublic?: boolean;
  status?: "draft" | "published" | "archived" | "active" | "inactive";

  tags?: string[];
  acts?: string[];
  dateUploaded?: Date;

  /** for timestamps */
  createdAt?: Date;
  updatedAt?: Date;

  extractTextContent(): void;
}

/* ======================================================================== */
/* 🧩 Model Statics Interface                                               */
/* ======================================================================== */

export interface IJudgmentModel extends Model<IJudgment> {
  getPendingAnalysis(page?: number, limit?: number): Promise<any>;
  getRecentlyCompleted(page?: number, limit?: number): Promise<any>;
  getFailedAnalysis(page?: number, limit?: number): Promise<any>;
  getAnalysisSummaryStats(): Promise<any>;
  getDashboardOverview(): Promise<any>;
}

/* ======================================================================== */
/* 🧩 Schema                                                                 */
/* ======================================================================== */

const PartiesSchema = new Schema<IParties>(
  {
    petitioner: { type: [String], default: [] },
    respondent: { type: [String], default: [] },
  },
  { _id: false }
);



const SectionRefSchema = new Schema<ISectionRef>(
  {
    section: { type: String, required: true },
    description: { type: String },
    linkedJudgments: [{ type: Schema.Types.ObjectId, ref: "Judgment" }],
  },
  { _id: false }
);

const ActReferenceSchema = new Schema<IActReference>(
  {
    actName: { type: String, required: true },
    sections: { type: [SectionRefSchema], default: [] },
    citations: { type: [String], default: [] },
    actId: { type: Schema.Types.ObjectId, ref: "Act" },
  },
  { _id: false }
);

const CitationSchema = new Schema<ICitation>(
  {
    caseName: String,
    citationText: String,
    citationType: {
      type: String,
      enum: [
        "overruled",
        "distinguished",
        "followed",
        "reversed",
        "reliedOn",
        "cited",
      ],
    },
    citationReference: String,
    judgmentId: { type: Schema.Types.Mixed },
  },
  { _id: false }
);

const FileRefSchema = new Schema<IFileRef>(
  {
    filename: { type: String, required: true },
    gridfsId: { type: Schema.Types.Mixed, required: true },
    fileId: { type: Schema.Types.Mixed },
  },
  { _id: false }
);

const PointOfLawSchema = new Schema<IPointOfLaw>(
  {
    principle: String,
    category: String,
    actReference: String,
    section: String,
  },
  { _id: false }
);

const JudgmentSchema = new Schema<IJudgment, IJudgmentModel>(
{
  parties: { type: PartiesSchema, required: true },

  amendedBy: { type: String, default: null },
  amendedAt: { type: Date, default: null },

  isOverruled: { type: Boolean, default: false },
  isPublic: { type: Boolean, default: true },

  tags: { type: [String], default: [] },
  acts: { type: [String], default: [] },

  status: {
    type: String,
    enum: ["draft", "published", "archived", "active", "inactive"],
    default: "active",
  },

  dateUploaded: { type: Date, default: Date.now },
},
{ timestamps: true }
);

JudgmentSchema.statics.getPendingAnalysis = async function (
  page = 1,
  limit = 20
) {
  const skip = (page - 1) * limit;
  const results = await this.find({ analysisStatus: "pending" })
    .sort({ createdAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();

  const total = await this.countDocuments({ analysisStatus: "pending" });
  return { results, total, page, limit, totalPages: Math.ceil(total / limit) };
};


JudgmentSchema.statics.getRecentlyCompleted = async function (
  page = 1,
  limit = 20
) {
  const skip = (page - 1) * limit;
  const results = await this.find({ analysisStatus: "completed" })
    .sort({ analysisCompletedAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();
  const total = await this.countDocuments({ analysisStatus: "completed" });
  return { results, total, page, limit, totalPages: Math.ceil(total / limit) };
};

JudgmentSchema.statics.getFailedAnalysis = async function (
  page = 1,
  limit = 20
) {
  const skip = (page - 1) * limit;
  const results = await this.find({ analysisStatus: "failed" })
    .sort({ updatedAt: -1 })
    .skip(skip)
    .limit(limit)
    .lean();
  const total = await this.countDocuments({ analysisStatus: "failed" });
  return { results, total, page, limit, totalPages: Math.ceil(total / limit) };
};

JudgmentSchema.statics.getDashboardOverview = async function () {
  const [summary, recent, failed] = await Promise.all([
    this.getAnalysisSummaryStats(),
    this.getRecentlyCompleted(1, 5),
    this.getFailedAnalysis(1, 5),
  ]);

  return {
    summary,
    recentCompleted: recent.results,
    recentFailed: failed.results,
  };
};

/* ======================================================================== */
/* 🧩 Export Model                                                           */
/* ======================================================================== */


export const Judgment = mongoose.model<IJudgment, IJudgmentModel>(
  "Judgment",
  JudgmentSchema
);

export default Judgment;
