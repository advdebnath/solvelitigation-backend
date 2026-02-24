import axios from "axios";
import Judgment from "../models/judgment.model";

export const retryPendingNLPJobs = async () => {
  const pending = await Judgment.find({
    nlpStatus: "PENDING",
  }).limit(10); // safety limit

  for (const judgment of pending) {
    try {
      // Call NLP service
      await axios.post("http://127.0.0.1:8000/enqueue", {
        jobId: judgment._id.toString(),
      });

      // Update DB safely without validation
      await Judgment.updateOne(
        { _id: judgment._id },
        {
          $set: {
            nlpStatus: "PROCESSING",
          },
        },
        { runValidators: false }
      );

      console.log(`✅ NLP requeued: ${judgment._id}`);
    } catch (err) {
      console.warn(`⚠️ NLP still unavailable for ${judgment._id}`);
    }
  }
};
