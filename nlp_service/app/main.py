from app.api.enqueue import router as enqueue_router
from fastapi import FastAPI

# ============================================
# 🔥 SAFE ROUTER IMPORTS
# ============================================


pdf_router = None
intelligent_router = None
prediction_router = None
legal_router = None

try:
    from app.api.pdf import router as pdf_router
except Exception as e:
    print("❌ pdf_router failed:", e)

try:
    from app.api.intelligent_engine import router as intelligent_router
except Exception as e:
    print("❌ intelligent_router failed:", e)

try:
    from app.api.prediction import router as prediction_router
except Exception as e:
    print("❌ prediction_router failed:", e)

try:
    from app.api.legal_gpt import router as legal_router
except Exception as e:
    print("❌ legal_router failed:", e)

from app.config import settings
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import build_index  # ✅ ADDED
from app.services.faiss_service import (fetch_documents, load_index,
                                        search_by_embedding)

# ============================================
# 🔥 FAISS + EMBEDDING
# ============================================



# ============================================
# ✅ APP
# ============================================

app = FastAPI(
    title="SolveLitigation NLP Service",
    version="2.4.0",
    docs_url="/docs",
    openapi_url="/openapi.json",
)

# ============================================
# 🚀 STARTUP
# ============================================


@app.on_event("startup")
def startup_event():
    print("🚀 NLP SERVICE STARTING...")

    try:
        load_index()
        print("✅ FAISS READY")
    except Exception as e:
        print("❌ FAISS ERROR:", e)

    print("✅ EMBEDDING READY (LAZY LOAD)")


# ============================================
# 🔥 ROUTES
# ============================================

app.include_router(enqueue_router, prefix="/api")

if pdf_router:
    app.include_router(pdf_router, prefix="/api")

if intelligent_router:
    app.include_router(intelligent_router, prefix="/api")

if prediction_router:
    app.include_router(prediction_router, prefix="/api")

if legal_router:
    app.include_router(legal_router, prefix="/api")

# ============================================
# ❤️ HEALTH
# ============================================


@app.get("/health")
def health():
    return {"status": "ok", "service": settings.NLP_SERVICE_NAME, "version": "2.4.0"}


# ============================================
# 🔍 FAISS SEARCH
# ============================================


@app.post("/faiss/search")
def faiss_search(data: dict):
    try:
        query = data.get("text", "")

        if not query or len(query) < 3:
            return {"success": True, "count": 0, "results": []}

        embedding = generate_embedding(query)

        if not embedding:
            return {"success": True, "count": 0, "results": []}

        results = search_by_embedding(embedding)
        docs = fetch_documents(results)

        return {"success": True, "count": len(docs), "results": docs}

    except Exception as e:
        print("❌ FAISS SEARCH ERROR:", e)
        return {"success": True, "count": 0, "results": []}


# ============================================
# 🔄 FAISS BUILD (CRITICAL FIX)
# ============================================


@app.get("/faiss/build")
def rebuild_faiss():
    try:
        print("🔄 Rebuilding FAISS index...")

        build_index()

        return {"success": True, "status": "rebuilt"}

    except Exception as e:
        import traceback

        traceback.print_exc()

        return {"success": False, "error": str(e)}


# ============================================
# ROOT
# ============================================


@app.get("/")
def root():
    return {"message": "NLP Service Running"}
