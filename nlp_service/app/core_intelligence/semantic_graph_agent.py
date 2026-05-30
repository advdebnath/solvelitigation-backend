# =========================================================
# 🔥 SEMANTIC GRAPH & VECTOR INTELLIGENCE AGENT
# =========================================================


def run_semantic_graph_analysis(
    reconstructed_text, constitutional_weight, semantic_confidence, procedural_timeline
):

    semantic_graph_intelligence = {
        "semantic_cluster": "GENERAL_DOCTRINE",
        "precedent_neighbors": [],
        "constitutional_density": 0.50,
        "graph_centrality_score": 0.50,
        "doctrine_evolution_topology": [],
        "issue_vector_similarity": 0.50,
    }

    try:

        upper_text = reconstructed_text.upper()

        doctrine_clusters = {
            "ARTICLE 21": "LIBERTY_CLUSTER",
            "ARTICLE 14": "EQUALITY_CLUSTER",
            "NATURAL JUSTICE": "FAIRNESS_CLUSTER",
            "PROPORTIONALITY": "PROPORTIONALITY_CLUSTER",
            "ARBITRARINESS": "ADMINISTRATIVE_CLUSTER",
            "BAIL": "CRIMINAL_LIBERTY_CLUSTER",
            "PREVENTIVE DETENTION": "DETENTION_CLUSTER",
        }

        semantic_cluster = "GENERAL_DOCTRINE"

        doctrine_evolution_topology = []

        for trigger, cluster in doctrine_clusters.items():

            if trigger in upper_text:

                semantic_cluster = cluster

                doctrine_evolution_topology.append(trigger)

        constitutional_density = round(
            (constitutional_weight + semantic_confidence) / 2, 2
        )

        graph_centrality_score = round(
            min(
                1.0, constitutional_density + (len(doctrine_evolution_topology) * 0.05)
            ),
            2,
        )

        issue_vector_similarity = round(
            (
                constitutional_density
                + (1 - procedural_timeline.get("appellate_delay_probability", 0.5))
            )
            / 2,
            2,
        )

        precedent_neighbors = []

        if semantic_cluster != "GENERAL_DOCTRINE":

            precedent_neighbors.append(semantic_cluster)

        semantic_graph_intelligence.update(
            {
                "semantic_cluster": semantic_cluster,
                "precedent_neighbors": precedent_neighbors,
                "constitutional_density": constitutional_density,
                "graph_centrality_score": graph_centrality_score,
                "doctrine_evolution_topology": doctrine_evolution_topology,
                "issue_vector_similarity": issue_vector_similarity,
            }
        )

    except Exception as e:

        print("❌ SEMANTIC GRAPH AGENT ERROR:")

        print(str(e))

    return semantic_graph_intelligence
