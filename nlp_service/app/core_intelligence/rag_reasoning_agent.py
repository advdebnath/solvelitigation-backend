# =========================================================
# 🔥 RETRIEVAL-AUGMENTED JURISPRUDENTIAL REASONING AGENT
# =========================================================


def run_rag_reasoning_analysis(
    citation_data,
    semantic_graph_intelligence,
    constitutional_weight,
    semantic_confidence,
):

    rag_reasoning = {
        "retrieved_precedents": [],
        "semantic_support_score": 0.50,
        "vector_grounding_strength": 0.50,
        "doctrine_alignment": 0.50,
        "memory_augmented_reasoning": False,
    }

    try:

        retrieved_precedents = []

        if isinstance(citation_data, list):

            for cite in citation_data[:5]:

                retrieved_precedents.append(
                    {
                        "precedent": str(cite),
                        "support_strength": round(semantic_confidence, 2),
                    }
                )

        constitutional_density = semantic_graph_intelligence.get(
            "constitutional_density", 0.50
        )

        graph_centrality_score = semantic_graph_intelligence.get(
            "graph_centrality_score", 0.50
        )

        semantic_support_score = round(
            (constitutional_density + graph_centrality_score + semantic_confidence) / 3,
            2,
        )

        vector_grounding_strength = round(
            (semantic_support_score + constitutional_weight) / 2, 2
        )

        doctrine_alignment = round(
            (constitutional_density + constitutional_weight) / 2, 2
        )

        memory_augmented_reasoning = len(retrieved_precedents) >= 2

        rag_reasoning.update(
            {
                "retrieved_precedents": retrieved_precedents,
                "semantic_support_score": semantic_support_score,
                "vector_grounding_strength": vector_grounding_strength,
                "doctrine_alignment": doctrine_alignment,
                "memory_augmented_reasoning": memory_augmented_reasoning,
            }
        )

    except Exception as e:

        print("❌ RAG REASONING AGENT ERROR:")

        print(str(e))

    return rag_reasoning
