import axios from "axios";

export async function enqueueNlpJob(judgmentId: string) {
const NLP_URL = process.env.NLP_BASE_URL;

if (!NLP_URL) {
  throw new Error("NLP_BASE_URL not configured");
}

  console.log("📤 Sending to NLP:", { judgmentId });

  await axios.post(
    `${NLP_URL}/api/enqueue`,
    { judgmentId },
    { timeout: 10000 }
  );
}
