import axios from "axios";

const NLP_URL = "http://127.0.0.1:8000";

export const fetchRelevantCases = async (query: string) => {
  try {
    const { data } = await axios.post(`${NLP_URL}/faiss/search`, {
      text: query,
    });

    if (!data.success) return [];

    return data.results.slice(0, 3); // top 3 cases

  } catch (err) {
    console.error("❌ Case-law fetch error:", err);
    return [];
  }
};
