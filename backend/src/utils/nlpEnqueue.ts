import axios from "axios";

interface EnqueuePayload {
  ingestionId: string;
  pdfPath: string;
}

export async function enqueueNlpJob(payload: EnqueuePayload) {
  const NLP_URL = process.env.NLP_SERVICE_URL;

  if (!NLP_URL) {
    throw new Error("NLP_SERVICE_URL not configured");
  }

  await axios.post(`${NLP_URL}/enqueue`, payload, {
    timeout: 10_000,
  });
}
