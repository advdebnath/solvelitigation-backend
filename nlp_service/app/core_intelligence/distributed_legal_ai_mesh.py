# =========================================================
# 🔥 DISTRIBUTED LEGAL AI MESH
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 GLOBAL MESH STATE
# =========================================================

LEGAL_AI_MESH = {
    "nodes": {},
    "node_roles": defaultdict(list),
    "node_health": {},
    "active_routes": [],
    "mesh_mode": "DISTRIBUTED_ACTIVE",
}

# =========================================================
# 🔥 REGISTER NODE
# =========================================================


def register_mesh_node(node_name, node_role):

    LEGAL_AI_MESH["nodes"][node_name] = {"role": node_role, "status": "ACTIVE"}

    LEGAL_AI_MESH["node_roles"][node_role].append(node_name)

    LEGAL_AI_MESH["node_health"][node_name] = 1.0

    return True


# =========================================================
# 🔥 UPDATE NODE HEALTH
# =========================================================


def update_node_health(node_name, health_score):

    LEGAL_AI_MESH["node_health"][node_name] = round(health_score, 2)

    # =====================================================
    # 🔥 FAILOVER DETECTION
    # =====================================================

    if health_score < 0.40:

        LEGAL_AI_MESH["nodes"][node_name]["status"] = "DEGRADED"

    return True


# =========================================================
# 🔥 REGISTER ROUTE
# =========================================================


def register_mesh_route(source_node, target_node, cognition_type):

    LEGAL_AI_MESH["active_routes"].append(
        {"source": source_node, "target": target_node, "cognition": cognition_type}
    )

    return True


# =========================================================
# 🔥 FETCH HEALTHY NODES
# =========================================================


def get_healthy_nodes():

    healthy = []

    for node, health in LEGAL_AI_MESH["node_health"].items():

        if health >= 0.60:

            healthy.append(node)

    return healthy


# =========================================================
# 🔥 FETCH MESH STATE
# =========================================================


def get_mesh_state():

    return LEGAL_AI_MESH
