"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.startWorker = startWorker;
const workers_1 = require("../../workers");
async function startWorker(req, res) {
    try {
        await (0, workers_1.planExpiryWorker)();
        return res.json({
            success: true,
            message: "Plan expiry worker executed successfully",
        });
    }
    catch (error) {
        console.error("[WORKER START ERROR]", error);
        return res.status(500).json({
            success: false,
            message: "Worker execution failed",
        });
    }
}
