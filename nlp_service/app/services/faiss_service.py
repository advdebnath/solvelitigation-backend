import faiss
import numpy as np
from bson import ObjectId
from pymongo import MongoClient

# ============================================
# 🔥 GLOBAL INDEX
# ============================================

index = None
id_map = []

# ============================================
# 🔥 DB CONNECTION
# ============================================

db = MongoClient("mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation")[
    "solvelitigation"
]

# ============================================
# 🔥 LOAD INDEX
# ============================================


def load_index():
    global index, id_map

    try:
        index = faiss.read_index("faiss.index")

        with open("faiss_ids.pkl", "rb") as f:
            import pickle

            id_map = pickle.load(f)

        print(f"✅ FAISS loaded ({len(id_map)} vectors)")

    except Exception:
        print("⚠️ No FAISS index found, building new...")
        build_index()


# ============================================
# 🔥 BUILD INDEX (CRITICAL FUNCTION)
# ============================================


def build_index():
    global index, id_map

    print("🔄 Building FAISS index from MongoDB...")

    docs = list(db.judgments.find({"embedding": {"$exists": True}}))

    if not docs:
        print("❌ No embeddings found in DB")
        return

    embeddings = []
    id_map = []

    for d in docs:
        emb = d.get("embedding")

        if emb and isinstance(emb, list):
            embeddings.append(emb)
            id_map.append(str(d["_id"]))

    if not embeddings:
        print("❌ No valid embeddings")
        return

    vectors = np.array(embeddings).astype("float32")

    # ✅ Normalize vectors before indexing
    import faiss

    faiss.normalize_L2(vectors)

    dim = vectors.shape[1]

    index = faiss.IndexFlatIP(dim)
    index.add(vectors)

    # Save
    faiss.write_index(index, "faiss.index")

    import pickle

    with open("faiss_ids.pkl", "wb") as f:
        pickle.dump(id_map, f)

    print(f"✅ Indexed {len(id_map)} documents")


# ============================================
# 🔍 SEARCH
# ============================================


def search_by_embedding(embedding, top_k=5):
    global index, id_map

    if index is None:
        return []

    import faiss
    import numpy as np

    vector = np.array([embedding]).astype("float32")

    # ✅ Normalize query vector
    faiss.normalize_L2(vector)

    scores, indices = index.search(vector, top_k)

    results = []

    for i, idx in enumerate(indices[0]):

        # ✅ skip invalid index
        if idx == -1:
            continue

        score = float(scores[0][i])

        # ✅ skip invalid scores
        if score <= 0:
            continue

        if idx < len(id_map):
            results.append({"id": id_map[idx], "score": score})

    return results


# ============================================
# 🔍 FETCH DOCS
# ============================================


def fetch_documents(results):
    docs = []

    for r in results:
        doc = db.judgments.find_one({"_id": ObjectId(r["id"])})

        if doc:
            docs.append(
                {
                    "caseNumber": doc.get("caseNumber"),
                    "headnote": doc.get("headnote") or doc.get("fullText", "")[:300],
                    "score": r["score"],
                }
            )

    return docs
