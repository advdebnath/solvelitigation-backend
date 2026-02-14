from fastapi import FastAPI
from app.api.enqueue import router as enqueue_router
from app.config import settings

app = FastAPI(
    title="SolveLitigation NLP Service",
    version="1.0.0",
)

# Routes
app.include_router(enqueue_router, prefix="/api")

@app.get("/health")
def health():
    return {
        "status": "ok",
        "service": settings.NLP_SERVICE_NAME,
    }
