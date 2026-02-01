/**
 * One-time script to enqueue all PENDING NLP judgments
 * Uses the SAME DB connection logic as the backend
 */

require("dotenv").config({
  path: process.env.NODE_ENV === "production"
    ? ".env.production"
    : ".env"
});

const { connectDB } = require("../dist/config/db");
const { Judgment } = require("../dist/models/judgment.model");
const { enqueueNlpJob } = require("../dist/utils/nlpEnqueue");

(async () => {
  try {
    console.log("🔌 Connecting to MongoDB...");
    await connectDB();

    console.log("📄 Fetching pending judgments...");
    const pending = await Judgment.find({ "nlp.status": "PENDING" });

    console.log(`📄 Found ${pending.length} pending judgments`);

    for (const j of pending) {
      await enqueueNlpJob({
        judgmentId: j._id.toString(),
      });

      console.log(`📤 Enqueued NLP job: ${j.title}`);
    }

    console.log("✅ All pending judgments enqueued");
    process.exit(0);
  } catch (err) {
    console.error(
      "❌ Failed to enqueue NLP jobs:",
      err.response?.data || err
    );
    process.exit(1);
  }
})();
