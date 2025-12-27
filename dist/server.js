"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
const express_1 = __importDefault(require("express"));
const http_1 = __importDefault(require("http"));
const cors_1 = __importDefault(require("cors"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const helmet_1 = __importDefault(require("helmet"));
const morgan_1 = __importDefault(require("morgan"));
const mongoose_1 = __importDefault(require("mongoose"));
// ROUTES (RELATIVE IMPORTS ONLY)
const auth_routes_1 = __importDefault(require("./routes/auth.routes"));
const health_routes_1 = __importDefault(require("./routes/health.routes"));
const judgments_routes_1 = __importDefault(require("./routes/judgments/judgments.routes"));
const acts_routes_1 = __importDefault(require("./routes/acts.routes"));
const judgment_upload_routes_1 = __importDefault(require("./routes/superadmin/judgment.upload.routes"));
const superadmin_1 = __importDefault(require("./routes/superadmin"));
const job_routes_1 = __importDefault(require("./routes/job.routes"));
const job_worker_1 = require("./workers/job.worker");
// -------------------- APP --------------------
const app = (0, express_1.default)();
app.set("trust proxy", 1);
const server = http_1.default.createServer(app);
// -------------------- MIDDLEWARES --------------------
app.use((0, cors_1.default)());
app.use(express_1.default.json({ limit: "20mb" })); // JSON payloads only
app.use(express_1.default.urlencoded({ extended: true, limit: "20mb" }));
// IMPORTANT: allow large multipart uploads (handled by multer)
app.set("maxFileSize", 900 * 1024 * 1024); // 900MB
app.use((0, cookie_parser_1.default)());
app.use((0, helmet_1.default)());
app.use((0, morgan_1.default)("dev"));
// -------------------- DATABASE --------------------
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/solvelitigation";
mongoose_1.default
    .connect(MONGO_URI)
    .then(() => console.log("✅ MongoDB connected"))
    .catch((err) => console.error("❌ MongoDB connection error:", err));
// -------------------- ROUTES --------------------
// 🔁 Background job worker (Phase 2)
setInterval(() => {
    (0, job_worker_1.processJobsSerially)().catch(err => console.error("[JOB_WORKER]", err));
}, 1000);
app.use("/api/health", health_routes_1.default);
app.use("/api/auth", auth_routes_1.default);
app.use("/api/judgments", judgments_routes_1.default);
app.use("/api/acts", acts_routes_1.default);
app.use("/api/superadmin/judgments", judgment_upload_routes_1.default);
app.use("/api/superadmin", superadmin_1.default);
app.use("/api/jobs", job_routes_1.default);
// -------------------- START SERVER --------------------
const PORT = Number(process.env.PORT) || 4000;
server.listen(PORT, "0.0.0.0", () => {
    console.log(`[boot] server listening on http://0.0.0.0:${PORT}`);
});
