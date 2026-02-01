import axios from "axios";

const NLP_BASE_URL =
  process.env.NLP_BASE_URL || "http://127.0.0.1:8000";

export interface EnqueueNlpJobPayload {
  jobId?: string;        // backward compatibility
  judgmentId?: string;  // preferred
  lockId?: string;      // 🔐 required for callback lock
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
      timeout: 30000,
    }
  );

  return res.data;
}
