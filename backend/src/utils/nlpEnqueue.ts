import axios from "axios";

export async function enqueueNlpJob(ingestionId: string) {
  const NLP_URL = process.env.NLP_BASE_URL;

  if (!NLP_URL) {
    throw new Error("NLP_BASE_URL not configured");
  }

  console.log("📤 Sending to NLP:", { ingestionId });

  await axios.post(
    `${NLP_URL}/api/enqueue`,
    { ingestionId },
    { timeout: 10000 }
  );
}
