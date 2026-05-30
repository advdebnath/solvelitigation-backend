# (from fastapi import APIRouter
import logging
from typing import Optional, Union

# 🔥 NEW ENGINE
from app.services.semantic_engine import (build_argument, generate_answer,
                                          semantic_search)
from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()
logger = logging.getLogger(__name__)

# ============================================
# 🔥 SAFE IMPORTS
# ============================================


def safe_import():
    global predict_advanced, predict, predict_with_judge
    global ADVANCED_AVAILABLE, JUDGE_AVAILABLE

    ADVANCED_AVAILABLE = False
    JUDGE_AVAILABLE = False
    predict = None

    try:
        from app.ml.predict_advanced import predict_advanced

        ADVANCED_AVAILABLE = True
        logger.info("✅ Advanced model loaded")
    except Exception as e:
        logger.warning(f"⚠️ Advanced model not available: {e}")

    try:
        from app.ml.predict import predict

        logger.info("✅ Basic model loaded")
    except Exception as e:
        logger.error(f"❌ Basic model missing: {e}")

    try:
        from app.ml.judge_predict import predict_with_judge

        JUDGE_AVAILABLE = True
        logger.info("✅ Judge model loaded")
    except Exception as e:
        logger.warning(f"⚠️ Judge model not available: {e}")


safe_import()

# ============================================
# 🔥 REQUEST MODELS
# ============================================


class PredictRequest(BaseModel):
    text: str
    judge: Optional[str] = None


class QueryRequest(BaseModel):
    query: str


# ============================================
# 🔥 HELPERS
# ============================================


def normalize_probability(value: Union[int, float, None]) -> int:
    try:
        if value is None:
            return 50

        value = float(value)

        if value <= 1:
            value = value * 100

        return max(0, min(100, int(value)))

    except Exception:
        return 50


# ============================================
# 🔥 PREDICTION API
# ============================================


@router.post("/predict-outcome")
async def predict_outcome(req: PredictRequest):
    try:
        text = req.text.strip()

        if not text or len(text) < 5:
            return {"success": False, "message": "Invalid input text"}

        ml_prob_raw = None
        model_used = "fallback"

        try:
            if ADVANCED_AVAILABLE:
                ml_prob_raw = predict_advanced(text)
                model_used = "embedding"
            elif predict:
                ml_prob_raw = predict(text)
                model_used = "basic"
        except Exception as e:
            logger.error(f"❌ ML prediction failed: {e}")

        ml_prob = normalize_probability(ml_prob_raw)

        judge_prob = None
        if JUDGE_AVAILABLE and req.judge:
            try:
                judge_raw = predict_with_judge(req.judge)
                judge_prob = normalize_probability(judge_raw)
            except Exception as e:
                logger.warning(f"⚠️ Judge prediction error: {e}")

        final_prob = ml_prob
        if judge_prob is not None:
            final_prob = int((ml_prob * 0.7) + (judge_prob * 0.3))

        label = "Win" if final_prob > 50 else "Lose"

        confidence = (
            "High" if final_prob > 75 else "Medium" if final_prob > 55 else "Low"
        )

        return {
            "success": True,
            "prediction": {
                "mlProbability": ml_prob,
                "judgeProbability": judge_prob,
                "finalProbability": final_prob,
                "label": label,
                "confidence": confidence,
                "model": "ml+judge" if judge_prob else model_used,
            },
        }

    except Exception as e:
        logger.exception("❌ CRITICAL ERROR")
        return {"success": False, "error": str(e)}


# ============================================
# 🔥 🔥 INTELLIGENT LEGAL ENGINE APIs
# ============================================


@router.post("/semantic/search")
async def semantic_search_api(req: QueryRequest):
    try:
        results = semantic_search(req.query)
        return {"success": True, "results": results}
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": str(e)}


@router.post("/semantic/answer")
async def semantic_answer_api(req: QueryRequest):
    try:
        answer = generate_answer(req.query)
        return {"success": True, "answer": answer}
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": str(e)}


@router.post("/semantic/argument")
async def semantic_argument_api(req: QueryRequest):
    try:
        arguments = build_argument(req.query)
        return {"success": True, "arguments": arguments}
    except Exception as e:
        logger.error(e)
        return {"success": False, "error": str(e)}
