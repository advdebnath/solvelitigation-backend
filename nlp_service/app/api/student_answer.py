# ============================================
# 🔥 NEW FAISS + EMBEDDING (UPDATED)
# ============================================
from app.services.embedding_service import generate_embedding
from app.services.faiss_service import fetch_documents, search_by_embedding
from fastapi import APIRouter
from pymongo import MongoClient

router = APIRouter()

db = MongoClient("mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation")[
    "solvelitigation"
]


# ============================================
# 🔥 STUDENT ANSWER ENGINE
# ============================================
@router.post("/student-answer")
def student_answer(data: dict):
    try:
        query = data.get("text", "")

        if not query or len(query) < 3:
            return {"success": False, "answer": "Invalid question"}

        # ============================================
        # 🔥 STEP 1: EMBEDDING
        # ============================================
        embedding = generate_embedding(query)

        if not embedding:
            return {"success": True, "answer": "No embedding generated"}

        # ============================================
        # 🔥 STEP 2: FAISS SEARCH
        # ============================================
        results = search_by_embedding(embedding, top_k=5)

        if not results:
            return {"success": True, "answer": "No relevant material found"}

        # ============================================
        # 🔥 STEP 3: FETCH FULL DOCUMENTS
        # ============================================
        docs = fetch_documents(results)

        if not docs:
            return {"success": True, "answer": "No valid documents found"}

        # ============================================
        # 🔥 STEP 4: EXTRACT CONTENT
        # ============================================
        headnotes = []
        points = set()
        cases = []

        for d in docs:
            if d.get("headnote"):
                headnotes.append(d["headnote"])

            if d.get("pointsOfLaw"):
                points.update(d["pointsOfLaw"])

            if d.get("caseNumber"):
                cases.append(d["caseNumber"])

        # limit
        headnotes = headnotes[:3]
        cases = list(dict.fromkeys(cases))[:3]

        # ============================================
        # 🔥 STEP 5: BUILD ANSWER
        # ============================================
        answer = f"""
📘 Answer:

This question relates to the legal principles concerning:

👉 {", ".join(points) if points else "general legal issues"}.

🔍 Explanation:
{" ".join(headnotes) if headnotes else "No detailed explanation available."}

📚 Case References:
{", ".join(cases) if cases else "No case references found."}
""".strip()

        return {
            "success": True,
            "answer": answer,
            "sources": cases,
            "confidence": round(results[0]["score"], 3),
        }

    except Exception as e:
        print("❌ STUDENT ANSWER ERROR:", e)
        return {"success": False, "error": str(e)}
