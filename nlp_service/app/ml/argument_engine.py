from app.ml.similarity_engine import find_similar_cases


# =========================================
# 🔥 BUILD ARGUMENT ENGINE
# =========================================
def build_arguments(text):
    similar_cases = find_similar_cases(text, top_k=5)

    if not similar_cases:
        return {"arguments": [], "citations": [], "reasoning": []}

    arguments = []
    citations = []
    reasoning = []

    for case in similar_cases:
        case_number = case.get("caseNumber")

        # 🔥 CITATION
        if case_number:
            citations.append(case_number)

        # 🔥 HEADNOTE AS ARGUMENT BASE
        if case.get("headnote"):
            arguments.append(case["headnote"])

        # 🔥 KEY PARAGRAPHS (STRONG REASONING)
        for kp in case.get("keyParagraphs", []):
            reasoning.append(
                {
                    "case": case_number,
                    "para": kp.get("para"),
                    "text": kp.get("text")[:500],
                }
            )

    return {
        "arguments": list(set(arguments)),
        "citations": list(set(citations)),
        "reasoning": reasoning[:10],
    }
