"use strict";
// FILE: backend/src/server.ts
// ✅ Production-stable server.ts
var __importDefault = (this && this.__importDefault) || function (mod) {
    return (mod && mod.__esModule) ? mod : { "default": mod };
};
Object.defineProperty(exports, "__esModule", { value: true });
exports.io = void 0;
const express_1 = __importDefault(require("express"));
const http_1 = __importDefault(require("http"));
const cors_1 = __importDefault(require("cors"));
const cookie_parser_1 = __importDefault(require("cookie-parser"));
const helmet_1 = __importDefault(require("helmet"));
const morgan_1 = __importDefault(require("morgan"));
const auth_routes_1 = __importDefault(require("./routes/auth.routes"));
const health_routes_1 = __importDefault(require("./routes/health.routes"));
// ------------------------------------------------------
// 🌐 Express app & HTTP server
// ------------------------------------------------------
const app = (0, express_1.default)();
const server = http_1.default.createServer(app);
// ------------------------------------------------------
// 🔒 Auth safety check – fail fast if bcrypt is missing
// ------------------------------------------------------
try {
    require('bcrypt');
}
catch {
    console.error('❌ bcrypt is missing – authentication cannot work');
}
// ------------------------------------------------------
// 🧩 MIDDLEWARES
// ------------------------------------------------------
app.use((0, cors_1.default)());
app.use(express_1.default.json({ limit: '50mb' }));
app.use(express_1.default.urlencoded({ extended: true }));
app.use((0, cookie_parser_1.default)());
app.use((0, helmet_1.default)());
app.use((0, morgan_1.default)('dev'));
// ------------------------------------------------------
// 🚏 ROUTES
// ------------------------------------------------------
app.use('/api/health', health_routes_1.default);
app.use('/api/auth', auth_routes_1.default);
// ------------------------------------------------------
// 🚀 START SERVER
// ------------------------------------------------------
const PORT = Number(process.env.PORT) || 4000;
if (!module.parent) {
    server.listen(PORT, '0.0.0.0', () => {
        console.log(`[boot] server listening on http://0.0.0.0:${PORT}`);
    });
}
exports.default = app;
