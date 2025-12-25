"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.startJudgmentWorker = startJudgmentWorker;
const workers_1 = require("../../workers");
async function startJudgmentWorker() {
    await (0, workers_1.processJobsSerially)();
}
