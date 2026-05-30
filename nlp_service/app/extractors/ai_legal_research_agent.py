import re

# =========================================================
# 🔥 CLEAN
# =========================================================


def clean_text(text):

    text = re.sub(r"\s+", " ", str(text))

    return text.strip()


# =========================================================
# 🔥 BUILD RESEARCH SUMMARY
# =========================================================


def build_research_summary(
    semantic_data=None,
    doctrine_data=None,
    reasoning_data=None,
    recommendation_data=None,
):

    parts = []

    # =====================================================
    # 🔥 SEMANTIC MEMORY
    # =====================================================

    if semantic_data:

        similar = semantic_data.get("similar_cases", [])

        if similar:

            parts.append(
                f"{len(similar)} semantically related judgments were identified."
            )

    # =====================================================
    # 🔥 DOCTRINE EVOLUTION
    # =====================================================

    if doctrine_data:

        doctrines = doctrine_data.get("doctrine_evolution", [])

        doctrine_names = []

        for d in doctrines[:5]:

            doctrine = d.get("doctrine")

            if doctrine:

                doctrine_names.append(doctrine)

        if doctrine_names:

            parts.append(
                "Important doctrines include " + ", ".join(doctrine_names) + "."
            )

    # =====================================================
    # 🔥 MULTI-CASE REASONING
    # =====================================================

    if reasoning_data:

        reasoning = reasoning_data.get("multi_case_reasoning")

        if reasoning:

            parts.append(reasoning)

    # =====================================================
    # 🔥 RECOMMENDATIONS
    # =====================================================

    if recommendation_data:

        recommendations = recommendation_data.get("recommendations", [])

        if recommendations:

            parts.append(
                "Recommended litigation strategy includes: " + recommendations[0]
            )

    return " ".join(parts)


# =========================================================
# 🔥 GENERATE LEGAL RESEARCH ANSWER
# =========================================================


def generate_ai_legal_research(
    query,
    semantic_data=None,
    doctrine_data=None,
    reasoning_data=None,
    recommendation_data=None,
):

    try:

        summary = build_research_summary(
            semantic_data=semantic_data,
            doctrine_data=doctrine_data,
            reasoning_data=reasoning_data,
            recommendation_data=recommendation_data,
        )

        # =================================================
        # 🔥 BUILD ANSWER
        # =================================================

        answer = f"Research Query: {query}. " + summary

        answer = clean_text(answer)

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {"research_query": query, "answer": answer, "confidence": 95}

        print("✅ AI Legal Research Generated:")

        print(result)

        return result

    except Exception as e:

        print("❌ AI Research Error:", str(e))

        return {"research_query": query, "answer": "", "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    semantic_data = {"similar_cases": [{"id": 1}, {"id": 2}]}

    doctrine_data = {
        "doctrine_evolution": [
            {"doctrine": "natural justice"},
            {"doctrine": "due process"},
        ]
    }

    reasoning_data = {
        "multi_case_reasoning": "Courts progressively expanded procedural fairness into constitutional due process."
    }

    recommendation_data = {"recommendations": ["Focus on procedural fairness."]}

    print(
        generate_ai_legal_research(
            query="natural justice in wakf disputes",
            semantic_data=semantic_data,
            doctrine_data=doctrine_data,
            reasoning_data=reasoning_data,
            recommendation_data=recommendation_data,
        )
    )
