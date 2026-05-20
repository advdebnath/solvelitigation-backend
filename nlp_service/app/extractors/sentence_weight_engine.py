from typing import Dict


# =========================================================
# 🔥 ROLE BASED WEIGHTS
# =========================================================

ROLE_WEIGHTS = {

    "OPERATIVE": {

        "importance_score": 95,
        "ratio_probability": 70,
        "operative_probability": 95,
        "precedent_weight": 85,
        "doctrinal_weight": 40,
        "binding_strength": 95,
    },

    "PRECEDENT": {

        "importance_score": 85,
        "ratio_probability": 80,
        "operative_probability": 20,
        "precedent_weight": 95,
        "doctrinal_weight": 75,
        "binding_strength": 90,
    },

    "DOCTRINE": {

        "importance_score": 80,
        "ratio_probability": 85,
        "operative_probability": 10,
        "precedent_weight": 70,
        "doctrinal_weight": 95,
        "binding_strength": 80,
    },

    "ANALYSIS": {

        "importance_score": 75,
        "ratio_probability": 90,
        "operative_probability": 20,
        "precedent_weight": 65,
        "doctrinal_weight": 70,
        "binding_strength": 75,
    },

    "ISSUE": {

        "importance_score": 65,
        "ratio_probability": 40,
        "operative_probability": 5,
        "precedent_weight": 40,
        "doctrinal_weight": 30,
        "binding_strength": 40,
    },

    "ARGUMENT": {

        "importance_score": 50,
        "ratio_probability": 25,
        "operative_probability": 5,
        "precedent_weight": 20,
        "doctrinal_weight": 20,
        "binding_strength": 15,
    },

    "FACT": {

        "importance_score": 35,
        "ratio_probability": 10,
        "operative_probability": 0,
        "precedent_weight": 5,
        "doctrinal_weight": 0,
        "binding_strength": 5,
    },

    "UNKNOWN": {

        "importance_score": 20,
        "ratio_probability": 10,
        "operative_probability": 0,
        "precedent_weight": 10,
        "doctrinal_weight": 10,
        "binding_strength": 10,
    }
}


# =========================================================
# 🔥 MAIN WEIGHT ENGINE
# =========================================================

def compute_sentence_weights(
    role_result: Dict
) -> Dict:

    if not role_result:

        return ROLE_WEIGHTS["UNKNOWN"]

    role = role_result.get(
        "role",
        "UNKNOWN"
    )

    weights = ROLE_WEIGHTS.get(

        role,

        ROLE_WEIGHTS["UNKNOWN"]
    )

    return {

        "role": role,

        "importance_score":
            weights["importance_score"],

        "ratio_probability":
            weights["ratio_probability"],

        "operative_probability":
            weights["operative_probability"],

        "precedent_weight":
            weights["precedent_weight"],

        "doctrinal_weight":
            weights["doctrinal_weight"],

        "binding_strength":
            weights["binding_strength"],
    }
