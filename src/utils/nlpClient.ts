import axios from "axios";

const NLP_SERVICE_URL =
  process.env.NLP_SERVICE_URL || "http://127.0.0.1:8000";

export async function enqueueNlpJob(payload: any) {
  const res = await axios.post(
    `${NLP_SERVICE_URL}/enqueue`,
    payload,
    { timeout: 30000 }
  );

  return res.data;
}
