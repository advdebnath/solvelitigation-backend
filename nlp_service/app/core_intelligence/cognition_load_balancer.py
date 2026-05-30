# =========================================================
# 🔥 COGNITION LOAD BALANCER
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 GLOBAL LOAD STATE
# =========================================================

COGNITION_LOAD_STATE = {
    "node_loads": defaultdict(float),
    "routing_history": [],
    "load_balancing_mode": "ADAPTIVE",
    "rebalance_events": [],
}

# =========================================================
# 🔥 UPDATE NODE LOAD
# =========================================================


def update_node_load(node_name, load_score):

    COGNITION_LOAD_STATE["node_loads"][node_name] = round(load_score, 2)

    return True


# =========================================================
# 🔥 SELECT BEST NODE
# =========================================================


def select_optimal_node(mesh_state, required_role=None):

    best_node = None

    best_score = 999

    try:

        nodes = mesh_state.get("nodes", {})

        node_health = mesh_state.get("node_health", {})

        for node_name, node_info in nodes.items():

            role = node_info.get("role")

            status = node_info.get("status")

            if status != "ACTIVE":

                continue

            if required_role and role != required_role:

                continue

            health = node_health.get(node_name, 0.50)

            load = COGNITION_LOAD_STATE["node_loads"].get(node_name, 0.50)

            # =================================================
            # 🔥 COMPUTE BALANCE SCORE
            # =================================================

            balance_score = load - (health * 0.5)

            if balance_score < best_score:

                best_score = balance_score

                best_node = node_name

        if best_node:

            COGNITION_LOAD_STATE["routing_history"].append(
                {
                    "selected_node": best_node,
                    "required_role": required_role,
                    "balance_score": round(best_score, 2),
                }
            )

    except Exception as e:

        print("❌ LOAD BALANCER ERROR:")

        print(str(e))

    return best_node


# =========================================================
# 🔥 REBALANCE DETECTION
# =========================================================


def detect_rebalance_requirement():

    rebalance_required = False

    overloaded_nodes = []

    try:

        for node, load in COGNITION_LOAD_STATE["node_loads"].items():

            if load >= 0.85:

                overloaded_nodes.append(node)

        if overloaded_nodes:

            rebalance_required = True

            COGNITION_LOAD_STATE["rebalance_events"].append(
                {"overloaded_nodes": overloaded_nodes}
            )

    except Exception as e:

        print("❌ REBALANCE DETECTION ERROR:")

        print(str(e))

    return {
        "rebalance_required": rebalance_required,
        "overloaded_nodes": overloaded_nodes,
    }


# =========================================================
# 🔥 FETCH LOAD STATE
# =========================================================


def get_load_balancer_state():

    return COGNITION_LOAD_STATE
