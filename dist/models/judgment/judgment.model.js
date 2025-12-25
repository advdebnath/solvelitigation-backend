"use strict";
var __createBinding = (this && this.__createBinding) || (Object.create ? (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    var desc = Object.getOwnPropertyDescriptor(m, k);
    if (!desc || ("get" in desc ? !m.__esModule : desc.writable || desc.configurable)) {
      desc = { enumerable: true, get: function() { return m[k]; } };
    }
    Object.defineProperty(o, k2, desc);
}) : (function(o, m, k, k2) {
    if (k2 === undefined) k2 = k;
    o[k2] = m[k];
}));
var __setModuleDefault = (this && this.__setModuleDefault) || (Object.create ? (function(o, v) {
    Object.defineProperty(o, "default", { enumerable: true, value: v });
}) : function(o, v) {
    o["default"] = v;
});
var __importStar = (this && this.__importStar) || (function () {
    var ownKeys = function(o) {
        ownKeys = Object.getOwnPropertyNames || function (o) {
            var ar = [];
            for (var k in o) if (Object.prototype.hasOwnProperty.call(o, k)) ar[ar.length] = k;
            return ar;
        };
        return ownKeys(o);
    };
    return function (mod) {
        if (mod && mod.__esModule) return mod;
        var result = {};
        if (mod != null) for (var k = ownKeys(mod), i = 0; i < k.length; i++) if (k[i] !== "default") __createBinding(result, mod, k[i]);
        __setModuleDefault(result, mod);
        return result;
    };
})();
Object.defineProperty(exports, "__esModule", { value: true });
exports.Judgment = void 0;
// backend/src/models/judgment.model.ts
const mongoose_1 = __importStar(require("mongoose"));
/* ======================================================================== */
/* 🧩 Schema                                                                 */
/* ======================================================================== */
const PartiesSchema = new mongoose_1.Schema({
    petitioner: { type: [String], default: [] },
    respondent: { type: [String], default: [] },
}, { _id: false });
const SectionRefSchema = new mongoose_1.Schema({
    section: { type: String, required: true },
    description: { type: String },
    linkedJudgments: [{ type: mongoose_1.Schema.Types.ObjectId, ref: "Judgment" }],
}, { _id: false });
const ActReferenceSchema = new mongoose_1.Schema({
    actName: { type: String, required: true },
    sections: { type: [SectionRefSchema], default: [] },
    citations: { type: [String], default: [] },
    actId: { type: mongoose_1.Schema.Types.ObjectId, ref: "Act" },
}, { _id: false });
const CitationSchema = new mongoose_1.Schema({
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
    judgmentId: { type: mongoose_1.Schema.Types.Mixed },
}, { _id: false });
const FileRefSchema = new mongoose_1.Schema({
    filename: { type: String, required: true },
    gridfsId: { type: mongoose_1.Schema.Types.Mixed, required: true },
    fileId: { type: mongoose_1.Schema.Types.Mixed },
}, { _id: false });
const PointOfLawSchema = new mongoose_1.Schema({
    principle: String,
    category: String,
    actReference: String,
    section: String,
}, { _id: false });
const JudgmentSchema = new mongoose_1.Schema({
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
}, { timestamps: true });
JudgmentSchema.statics.getPendingAnalysis = async function (page = 1, limit = 20) {
    const skip = (page - 1) * limit;
    const results = await this.find({ analysisStatus: "pending" })
        .sort({ createdAt: -1 })
        .skip(skip)
        .limit(limit)
        .lean();
    const total = await this.countDocuments({ analysisStatus: "pending" });
    return { results, total, page, limit, totalPages: Math.ceil(total / limit) };
};
JudgmentSchema.statics.getRecentlyCompleted = async function (page = 1, limit = 20) {
    const skip = (page - 1) * limit;
    const results = await this.find({ analysisStatus: "completed" })
        .sort({ analysisCompletedAt: -1 })
        .skip(skip)
        .limit(limit)
        .lean();
    const total = await this.countDocuments({ analysisStatus: "completed" });
    return { results, total, page, limit, totalPages: Math.ceil(total / limit) };
};
JudgmentSchema.statics.getFailedAnalysis = async function (page = 1, limit = 20) {
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
exports.Judgment = mongoose_1.default.model("Judgment", JudgmentSchema);
exports.default = exports.Judgment;
