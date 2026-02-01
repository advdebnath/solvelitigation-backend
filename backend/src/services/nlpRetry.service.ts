import axios from "axios";
import { Judgment } from "../models/judgment.model";

export const retryPendingNLPJobs = async () => {
  const pending = await Judgment.find({
    "nlp.status": "PENDING",
  }).limit(10); // safety limit

  for (const judgment of pending) {
    try {
      await axios.post("http://127.0.0.1:8000/enqueue", {
        jobId: judgment._id.toString(),
      });

      judgment.nlp.status = "PROCESSING";
      await judgment.save();

      console.log(`✅ NLP requeued: ${judgment._id}`);
    } catch {
      console.warn(`⚠️ NLP still unavailable for ${judgment._id}`);
    }
  }
};
