"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.requestLogger = requestLogger;
function requestLogger(req, _res, next) {
    console.log(`[${req.method}] ${req.originalUrl}`);
    next();
}
