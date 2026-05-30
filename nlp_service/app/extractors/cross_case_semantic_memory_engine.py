import os
import pickle

import faiss
import numpy as np
from sentence_transformers import SentenceTransformer

# =========================================================
# 🔥 PATHS
# =========================================================

BASE_DIR = "/var/www/solvelitigation/nlp_service"

FAISS_INDEX_PATH = os.path.join(BASE_DIR, "faiss.index")

FAISS_IDS_PATH = os.path.join(BASE_DIR, "faiss_ids.pkl")


# =========================================================
# 🔥 LOAD MODEL
# =========================================================

MODEL = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")


# =========================================================
# 🔥 LOAD FAISS
# =========================================================


def load_faiss():

    if not os.path.exists(FAISS_INDEX_PATH):

        return None, []

    index = faiss.read_index(FAISS_INDEX_PATH)

    ids = []

    if os.path.exists(FAISS_IDS_PATH):

        with open(FAISS_IDS_PATH, "rb") as f:

            ids = pickle.load(f)

    return index, ids


# =========================================================
# 🔥 BUILD LEGAL MEMORY TEXT
# =========================================================


def build_memory_text(
    headnote=None, issue_data=None, ratio_data=None, legal_gpt_data=None
):

    parts = []

    if headnote:

        parts.append(str(headnote))

    if issue_data:

        dominant = issue_data.get("dominant_issue")

        if dominant:

            parts.append(dominant)

    if ratio_data:

        ratios = ratio_data.get("ratio_decidendi", [])

        for r in ratios[:2]:

            ratio = r.get("ratio")

            if ratio:

                parts.append(ratio)

    if legal_gpt_data:

        analysis = legal_gpt_data.get("legal_analysis")

        if analysis:

            parts.append(analysis)

    return " ".join(parts)


# =========================================================
# 🔥 SEARCH SIMILAR CASES
# =========================================================


def search_similar_cases(memory_text, top_k=5):

    try:

        index, ids = load_faiss()

        if index is None:

            return {"similar_cases": [], "confidence": 0}

        embedding = MODEL.encode([memory_text], convert_to_numpy=True)

        embedding = np.array(embedding, dtype=np.float32)

        distances, indexes = index.search(embedding, top_k)

        results = []

        for score, idx in zip(distances[0], indexes[0]):

            if idx >= len(ids):

                continue

            results.append(
                {"judgment_id": str(ids[idx]), "semantic_score": float(score)}
            )

        result = {"similar_cases": results, "confidence": 95}

        print("✅ Cross-Case Semantic Memory:")

        print(result)

        return result

    except Exception as e:

        print("❌ Semantic Memory Error:", str(e))

        return {"similar_cases": [], "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    issue_data = {"dominant_issue": "Natural Justice Violation"}

    ratio_data = {
        "ratio_decidendi": [{"ratio": "Natural justice requires fair hearing."}]
    }

    legal_gpt_data = {
        "legal_analysis": "The appeal is likely to succeed due to procedural unfairness."
    }

    memory_text = build_memory_text(
        headnote="Natural justice case",
        issue_data=issue_data,
        ratio_data=ratio_data,
        legal_gpt_data=legal_gpt_data,
    )

    print(search_similar_cases(memory_text))

# =========================================================
# 🔥 CONNECTED MEMORY WRAPPER
# =========================================================


def build_cross_case_semantic_memory(full_text, existing_cases=None):

    try:

        results = search_similar_cases(memory_text=full_text, top_k=5)

        return {
            "similar_cases": results.get("similar_cases", []),
            "confidence": results.get("confidence", 90),
        }

    except Exception as e:

        print("❌ Semantic Memory Wrapper Error:", str(e))

        return {"similar_cases": [], "confidence": 0}
