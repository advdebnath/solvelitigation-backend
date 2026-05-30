from app.services.document_parser import parse_document
# =========================================
# 🔥 CORE LEGAL ENGINE
# =========================================
from app.services.legal_gpt import generate_legal_answer, search_similar_cases
from app.services.legal_intelligence import build_legal_intelligence
from app.services.petition_engine import generate_petition
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()


# =========================================
# 🔥 REQUEST MODELS
# =========================================
class QueryRequest(BaseModel):
    query: str


class PetitionRequest(BaseModel):
    query: str
    text: str


# =========================================
# 🔥 LEGAL GPT (STABLE)
# =========================================
@router.post("/legal-gpt")
async def legal_gpt(req: QueryRequest):
    try:
        if not req.query:
            raise HTTPException(status_code=400, detail="Query is required")

        answer = generate_legal_answer(req.query)

        return {"success": True, "query": req.query, "answer": answer}

    except Exception as e:
        print("❌ Legal GPT Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))


# =========================================
# 🔥 PETITION ENGINE (UPGRADED SAFE)
# =========================================
@router.post("/draft-petition")
async def draft_petition(req: PetitionRequest):
    try:
        if not req.text:
            raise HTTPException(status_code=400, detail="Document text is required")

        # 🔥 STEP 1 — PARSE DOCUMENT
        structured = parse_document(req.text)

        # 🔥 STEP 2 — BUILD INTELLIGENCE
        intelligence = build_legal_intelligence(req.text)

        # 🔥 STEP 3 — FETCH CASES (SAFE VERSION)
        cases = search_similar_cases(req.query)

        # 🔥 STEP 4 — GENERATE PETITION
        petition = generate_petition(
            structured_docs=structured,
            query=req.query,
            precedents=cases,
            intelligence=intelligence,
        )

        return {
            "success": True,
            "query": req.query,
            "petition": petition,
            "structured": structured,
            "intelligence": intelligence,
            "cases_used": [c.get("caseNumber") for c in cases] if cases else [],
        }

    except Exception as e:
        print("❌ Petition Error:", str(e))
        raise HTTPException(status_code=500, detail=str(e))
