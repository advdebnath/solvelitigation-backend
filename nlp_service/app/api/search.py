from app.services.embedding_service import generate_embedding
from app.services.faiss_service import fetch_documents, search_by_embedding
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


# =========================================
# REQUEST MODEL
# =========================================
class SearchRequest(BaseModel):
    query: str
    top_k: int = 5


# =========================================
# 🔥 MAIN SEARCH API
# =========================================
@router.post("/search")
def search(req: SearchRequest):
    try:
        query = req.query.strip()

        if not query or len(query) < 3:
            return {"success": True, "results": []}

        # =========================================
        # 🔥 STEP 1: EMBEDDING
        # =========================================
        embedding = generate_embedding(query)

        if not embedding:
            return {"success": True, "results": []}

        # =========================================
        # 🔥 STEP 2: FAISS SEARCH
        # =========================================
        results = search_by_embedding(embedding, top_k=req.top_k)

        if not results:
            return {"success": True, "results": []}

        # =========================================
        # 🔥 STEP 3: FETCH FULL DOCUMENTS
        # =========================================
        final_results = fetch_documents(results)

        return {"success": True, "count": len(final_results), "results": final_results}

    except Exception as e:
        print("❌ SEARCH API ERROR:", e)
        return {"success": False, "error": str(e)}
