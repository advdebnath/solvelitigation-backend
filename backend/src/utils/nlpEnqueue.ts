import axios from "axios";

export async function enqueueNlpJob(ingestionId: string) {
  const NLP_URL = process.env.NLP_BASE_URL;

  if (!NLP_URL) {
    throw new Error("❌ NLP_BASE_URL not configured");
  }

  try {
    console.log("📤 Sending to NLP API:", {
      ingestionId,
      url: `${NLP_URL}/api/enqueue`,
    });

    const response = await axios.post(
      `${NLP_URL}/api/enqueue`,
      {
        ingestionId: ingestionId,
      },
      {
        timeout: 120000,
        headers: {
          "Content-Type": "application/json",
        },
      }
    );

    // ✅ Validate response
    if (!response?.data) {
      throw new Error("❌ Empty response from NLP API");
    }

    console.log("✅ NLP queued successfully:", response.data);

    return response.data;

  } catch (error: any) {
    console.error("❌ NLP enqueue failed:");

    if (error.response) {
      console.error("📥 Response error:", {
        status: error.response.status,
        data: error.response.data,
      });
    } else if (error.request) {
      console.error("📡 No response received from NLP API");
    } else {
      console.error("⚠️ Error:", error.message);
    }

    // 🔥 IMPORTANT: rethrow so retry logic works
    throw error;
  }
}
