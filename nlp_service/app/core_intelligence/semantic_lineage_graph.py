# =========================================================
# 🔥 SEMANTIC LINEAGE GRAPH ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 BUILD SEMANTIC LINEAGE GRAPH
# =========================================================

def build_semantic_lineage_graph(

    replay_data
):

    graph = {

        "nodes": [],

        "edges": [],

        "agent_relationships": defaultdict(list),

        "event_dependencies": defaultdict(list),

        "constitutional_paths": [],

        "semantic_clusters": defaultdict(list)
    }

    try:

        timeline = replay_data.get(
            "timeline",
            []
        )

        previous_node = None

        for idx, event in enumerate(timeline):

            node_id = f"node_{idx}"

            agent = event.get(
                "agent"
            )

            event_type = event.get(
                "event"
            )

            payload = event.get(
                "payload",
                {}
            )

            node = {

                "id":
                    node_id,

                "agent":
                    agent,

                "event":
                    event_type,

                "payload":
                    payload
            }

            graph["nodes"].append(node)

            # =================================================
            # 🔥 EDGE CREATION
            # =================================================

            if previous_node:

                edge = {

                    "source":
                        previous_node,

                    "target":
                        node_id,

                    "relationship":
                        "semantic_flow"
                }

                graph["edges"].append(edge)

            previous_node = node_id

            # =================================================
            # 🔥 AGENT RELATIONSHIPS
            # =================================================

            graph[
                "agent_relationships"
            ][agent].append(node_id)

            # =================================================
            # 🔥 EVENT DEPENDENCIES
            # =================================================

            graph[
                "event_dependencies"
            ][event_type].append(node_id)

            # =================================================
            # 🔥 CONSTITUTIONAL PATHS
            # =================================================

            if "constitutional" in event_type.lower():

                graph[
                    "constitutional_paths"
                ].append(node_id)

            # =================================================
            # 🔥 SEMANTIC CLUSTERS
            # =================================================

            cluster = "general"

            if "rag" in agent:

                cluster = "precedent"

            elif "strategy" in agent:

                cluster = "constitutional"

            elif "validation" in agent:

                cluster = "verification"

            elif "graph" in agent:

                cluster = "semantic"

            graph[
                "semantic_clusters"
            ][cluster].append(node_id)

        graph[
            "agent_relationships"
        ] = dict(
            graph["agent_relationships"]
        )

        graph[
            "event_dependencies"
        ] = dict(
            graph["event_dependencies"]
        )

        graph[
            "semantic_clusters"
        ] = dict(
            graph["semantic_clusters"]
        )

    except Exception as e:

        print(
            "❌ SEMANTIC LINEAGE GRAPH ERROR:"
        )

        print(str(e))

    return graph
