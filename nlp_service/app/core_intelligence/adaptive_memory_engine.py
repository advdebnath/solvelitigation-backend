# =========================================================
# 🔥 ADAPTIVE MEMORY ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 GLOBAL MEMORY STORE
# =========================================================

LEGAL_MEMORY = {
    "agent_memory": defaultdict(list),
    "constitutional_memory": [],
    "contradiction_memory": [],
    "precedent_memory": [],
    "semantic_clusters": defaultdict(list),
}

# =========================================================
# 🔥 STORE MEMORY
# =========================================================


def store_memory(agent_name, memory_type, payload):

    try:

        LEGAL_MEMORY["agent_memory"][agent_name].append(payload)

        if memory_type == "constitutional":

            LEGAL_MEMORY["constitutional_memory"].append(payload)

        elif memory_type == "contradiction":

            LEGAL_MEMORY["contradiction_memory"].append(payload)

        elif memory_type == "precedent":

            LEGAL_MEMORY["precedent_memory"].append(payload)

        elif memory_type == "semantic_cluster":

            cluster_name = payload.get("cluster", "general")

            LEGAL_MEMORY["semantic_clusters"][cluster_name].append(payload)

        return True

    except Exception as e:

        print("❌ MEMORY STORE ERROR:")

        print(str(e))

        return False


# =========================================================
# 🔥 FETCH AGENT MEMORY
# =========================================================


def get_agent_memory(agent_name):

    return LEGAL_MEMORY["agent_memory"].get(agent_name, [])


# =========================================================
# 🔥 FETCH CONSTITUTIONAL MEMORY
# =========================================================


def get_constitutional_memory():

    return LEGAL_MEMORY["constitutional_memory"]


# =========================================================
# 🔥 FETCH PRECEDENT MEMORY
# =========================================================


def get_precedent_memory():

    return LEGAL_MEMORY["precedent_memory"]


# =========================================================
# 🔥 FETCH SEMANTIC CLUSTER MEMORY
# =========================================================


def get_semantic_cluster_memory(cluster_name):

    return LEGAL_MEMORY["semantic_clusters"].get(cluster_name, [])


# =========================================================
# 🔥 MEMORY SUMMARY
# =========================================================


def get_memory_summary():

    return {
        "agents": len(LEGAL_MEMORY["agent_memory"]),
        "constitutional_events": len(LEGAL_MEMORY["constitutional_memory"]),
        "contradiction_events": len(LEGAL_MEMORY["contradiction_memory"]),
        "precedent_events": len(LEGAL_MEMORY["precedent_memory"]),
        "semantic_clusters": list(LEGAL_MEMORY["semantic_clusters"].keys()),
    }
