import axios from "axios";

const NLP_BASE_URL = process.env.NLP_BASE_URL || "http://127.0.0.1:8000";

export async function enqueueNlpJob(payload: {
  jobId: string;
  pdfPath: string;
  meta?: any;
}) {
  const res = await axios.post(
    `${NLP_BASE_URL}/enqueue`,
    payload,
    { timeout: 5000 }
  );

  return res.data;
}
