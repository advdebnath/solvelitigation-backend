from fastapi import APIRouter
from pymongo import MongoClient
from bson import ObjectId

from app.services.embedding_service import generate_embedding
from app.services.faiss_service import search_by_embedding, fetch_documents

router = APIRouter()

db = MongoClient(
    "mongodb://sl_app:Debnath%401966@127.0.0.1:27017/solvelitigation"
)["solvelitigation"]


# ============================================
# 🔥 INTENT DETECTION
# ============================================
def detect_intent(text: str):
    t = text.lower()

    if any(k in t for k in ["explain", "define"]):
        return "explanation"

    if any(k in t for k in ["discuss", "elaborate", "describe"]):
        return "long_answer"

    if any(k in t for k in ["argue", "whether", "justify"]):
        return "argument"

    return "short_answer"


# ============================================
# 🔥 SYNTHESIS
# ============================================
def synthesize(docs):
    points = set()
    explanations = []
    cases = []

    for d in docs:
        if d.get("pointsOfLaw"):
            points.update(d["pointsOfLaw"])

        if d.get("headnote"):
            explanations.append(d["headnote"])

        if d.get("caseNumber"):
            cases.append(d["caseNumber"])

    explanations = list(dict.fromkeys(explanations))[:2]
    cases = list(dict.fromkeys(cases))[:3]

    return {
        "topic": ", ".join(points) if points else "Legal Issue",
        "explanation": " ".join(explanations) if explanations else "No explanation available",
        "cases": cases
    }


# ============================================
# 🔥 GENERATORS
# ============================================
def generate_short(data):
    return f"""
📘 Topic:
{data['topic']}

🔹 Explanation:
{data['explanation']}

🔹 Case:
{data['cases'][0] if data['cases'] else "N/A"}
""".strip()


def generate_argument(data):
    return f"""
⚖️ Legal Argument:

In light of precedents such as {", ".join(data['cases']) if data['cases'] else "relevant authorities"},
it is submitted that the issue concerning {data['topic']} is governed by the principle that
{data['explanation']}.
""".strip()


def generate_irac(data, query):
    return f"""
⚖️ Issue:
Whether {query.lower().strip()}.

📜 Rule:
The issue is governed by principles relating to {data['topic']}.

🔍 Application:
{data['explanation']}

✅ Conclusion:
Thus, governed by precedents such as {', '.join(data['cases']) if data['cases'] else 'relevant case law'}.
""".strip()


def generate_counter_argument(data):
    return f"""
⚖️ Counter-Argument:

It may be argued that the statutory provision allows flexibility in interpretation.

However, such contention is weak in light of precedents such as {", ".join(data['cases']) if data['cases'] else "relevant cases"}.
""".strip()


def predict_outcome(data):
    if data["cases"]:
        return "Likely favourable based on precedent"
    return "Outcome uncertain"


def build_citation_links(data):
    return [
        {
            "case": c,
            "url": f"/judgment/search?citation={c.replace(' ', '%20')}"
        }
        for c in data["cases"]
    ]


def generate_full_argument(data, query):
    irac = generate_irac(data, query)
    counter = generate_counter_argument(data)
    outcome = predict_outcome(data)

    return f"""
{irac}

----------------------------------------

{counter}

----------------------------------------

⚖️ Likely Outcome:
{outcome}
""".strip()


# ============================================
# 🔥 MAIN API (UPDATED WITH FAISS)
# ============================================
@router.post("/intelligent-answer")
def intelligent_answer(data: dict):
    query = data.get("text", "")

    if not query or len(query) < 3:
        return {"success": False, "answer": "Invalid query"}

    intent = detect_intent(query)

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
        return {"success": True, "answer": "No relevant answer found"}

    # ============================================
    # 🔥 STEP 3: FETCH FULL DOCUMENTS
    # ============================================
    docs = fetch_documents(results)

    if not docs:
        return {"success": True, "answer": "No verified content available"}

    structured = synthesize(docs)

    confidence = round(results[0]["score"], 3) if results else 0

    # ============================================
    # 🔥 RESPONSE GENERATION
    # ============================================
    if intent == "argument":
        answer = generate_full_argument(structured, query)

    elif intent in ["long_answer", "explanation"]:
        answer = generate_irac(structured, query)

    else:
        answer = generate_short(structured)

    return {
        "success": True,
        "intent": intent,
        "confidence": confidence,
        "answer": answer,
        "sources": structured["cases"],
        "citations": build_citation_links(structured)
    }
