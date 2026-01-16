"use strict";
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
require("dotenv/config");
const express_1 = __importDefault(require("express"));
const http_1 = __importDefault(require("http"));
const cors_1 = __importDefault(require("cors"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const helmet_1 = __importDefault(require("helmet"));
const morgan_1 = __importDefault(require("morgan"));
const mongoose_1 = __importDefault(require("mongoose"));
const cleanupUnverifiedUsers_job_1 = require("./jobs/cleanupUnverifiedUsers.job");
// ROUTES
const auth_routes_1 = __importDefault(require("./routes/auth.routes"));
const health_routes_1 = __importDefault(require("./routes/health.routes"));
const judgments_routes_1 = __importDefault(require("./routes/judgments/judgments.routes"));
const acts_routes_1 = __importDefault(require("./routes/acts.routes"));
const superadmin_1 = __importDefault(require("./routes/superadmin"));
const users_routes_1 = __importDefault(require("./routes/superadmin/users.routes"));
const job_routes_1 = __importDefault(require("./routes/job.routes"));
const pricing_routes_1 = __importDefault(require("./routes/pricing.routes"));
const location_routes_1 = __importDefault(require("./routes/location.routes"));
const nlp_routes_1 = __importDefault(require("./routes/nlp.routes"));
const planExpiry_job_1 = require("./jobs/planExpiry.job");
// JOB WORKER
const job_worker_1 = require("./workers/job.worker");
const app = (0, express_1.default)();
app.set("trust proxy", 1);
const server = http_1.default.createServer(app);
/* --------------------------------------------------
   MIDDLEWARES
-------------------------------------------------- */
// CORS — MUST be before routes
app.use((0, cors_1.default)({
    origin: [
        "https://solvelitigation.com",
        "https://www.solvelitigation.com",
    ],
    credentials: true, // ✅ REQUIRED for HttpOnly auth cookies
}));
app.use(express_1.default.json({ limit: "900mb" }));
app.use(express_1.default.urlencoded({ extended: true, limit: "900mb" }));
app.set("maxFileSize", 900 * 1024 * 1024);
app.use((0, cookie_parser_1.default)());
app.use((0, helmet_1.default)());
app.use((0, morgan_1.default)("dev"));
/* --------------------------------------------------
   DATABASE
-------------------------------------------------- */
const MONGO_URI = process.env.MONGO_URI || "mongodb://127.0.0.1:27017/solvelitigation";
mongoose_1.default
    .connect(MONGO_URI)
    .then(() => {
    console.log("✅ MongoDB connected");
    (0, planExpiry_job_1.planExpiryJob)();
    // ✅ Start cron job ONCE
    (0, cleanupUnverifiedUsers_job_1.startCleanupUnverifiedUsersJob)();
})
    .catch((err) => {
    console.error("❌ MongoDB connection failed", err);
});
/* --------------------------------------------------
   BACKGROUND JOB WORKER
-------------------------------------------------- */
setInterval(() => {
    (0, job_worker_1.processJobsSerially)().catch((err) => console.error("[JOB_WORKER]", err));
}, 1000);
/* --------------------------------------------------
   ROUTES
-------------------------------------------------- */
app.use("/api/health", health_routes_1.default);
app.use("/api/auth", auth_routes_1.default);
app.use("/api/judgments", judgments_routes_1.default);
app.use("/api/nlp", nlp_routes_1.default);
app.use("/api/acts", acts_routes_1.default);
app.use("/api/superadmin", superadmin_1.default);
app.use("/api/superadmin", users_routes_1.default);
app.use("/api/jobs", job_routes_1.default);
app.use("/api/pricing", pricing_routes_1.default);
app.use("/api/location", location_routes_1.default);
/* --------------------------------------------------
   START SERVER
-------------------------------------------------- */
const PORT = Number(process.env.PORT) || 4000;
(async () => {
    try {
        console.log("✅ MongoDB connected");
        // 🔁 Start cron jobs AFTER DB is ready
        (0, cleanupUnverifiedUsers_job_1.startCleanupUnverifiedUsersJob)();
        app.listen(PORT, () => {
            console.log(`🚀 Server running on port ${PORT}`);
        });
    }
    catch (err) {
        console.error("❌ Server startup failed:", err);
        process.exit(1);
    }
})();
