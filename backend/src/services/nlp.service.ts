import axios from "axios";

const NLP_BASE_URL =
  process.env.NLP_BASE_URL || "http://127.0.0.1:8000";

export interface EnqueueNlpJobPayload {
  jobId?: string;        // backward compatible
  judgmentId?: string;  // preferred identifier
  lockId?: string;      // 🔐 required for duplicate callback lock
  pdfPath: string;
  meta?: any;
}

export async function enqueueNlpJob(
  payload: EnqueueNlpJobPayload
) {
  const res = await axios.post(
    `${NLP_BASE_URL}/enqueue`,
    payload,
    {
      timeout: 30000, // NLP enqueue can be slow
    }
  );

  return res.data;
}
