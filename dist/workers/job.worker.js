"use strict";
Object.defineProperty(exports, "__esModule", { value: true });
exports.processJobsSerially = void 0;
const job_model_1 = require("../models/job.model");
const upload_worker_1 = require("./upload.worker");
/**
 * Serial job processor with locking & recovery
 */
const processJobsSerially = async () => {
    const now = new Date();
    /**
     * 1️⃣ Recover stuck jobs (PROCESSING > 10 minutes)
     */
    await job_model_1.Job.updateMany({
        status: "PROCESSING",
        updatedAt: { $lt: new Date(Date.now() - 10 * 60 * 1000) },
    }, {
        $set: {
            status: "FAILED",
            error: "Job timed out",
        },
    });
    /**
     * 2️⃣ Atomically lock ONE pending job
     */
    const job = await job_model_1.Job.findOneAndUpdate({ status: "PENDING" }, {
        status: "PROCESSING",
        updatedAt: now,
    }, { new: true });
    if (!job)
        return;
    try {
        switch (job.type) {
            case "UPLOAD_JUDGMENTS":
                await (0, upload_worker_1.processUploadJob)(job._id.toString());
                break;
            default:
                throw new Error(`Unknown job type: ${job.type}`);
        }
        /**
         * 3️⃣ Mark success
         */
        await job_model_1.Job.findByIdAndUpdate(job._id, {
            status: "COMPLETED",
            progress: 100,
        });
    }
    catch (error) {
        /**
         * 4️⃣ Mark failure
         */
        await job_model_1.Job.findByIdAndUpdate(job._id, {
            status: "FAILED",
            error: error?.message || "Job execution failed",
        });
    }
};
exports.processJobsSerially = processJobsSerially;
