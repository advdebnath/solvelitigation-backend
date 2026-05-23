# =========================================================
# 🔥 DISTRIBUTED LEGAL AI AGENT REGISTRY
# =========================================================

from app.core_intelligence.self_validation_agent import (
    run_self_validation
)

from app.core_intelligence.evidentiary_agent import (
    run_evidentiary_analysis
)

from app.core_intelligence.procedural_timeline_agent import (
    run_procedural_timeline_analysis
)

from app.core_intelligence.semantic_graph_agent import (
    run_semantic_graph_analysis
)

from app.core_intelligence.rag_reasoning_agent import (
    run_rag_reasoning_analysis
)

from app.core_intelligence.agentic_reasoning_agent import (
    run_agentic_reasoning_analysis
)

from app.core_intelligence.strategy_orchestration_agent import (
    run_strategy_orchestration
)

# =========================================================
# 🔥 CENTRALIZED AGENT REGISTRY
# =========================================================

AGENT_REGISTRY = {

    "validation":
        run_self_validation,

    "evidentiary":
        run_evidentiary_analysis,

    "procedural":
        run_procedural_timeline_analysis,

    "semantic_graph":
        run_semantic_graph_analysis,

    "rag":
        run_rag_reasoning_analysis,

    "agentic":
        run_agentic_reasoning_analysis,

    "strategy":
        run_strategy_orchestration
}

# =========================================================
# 🔥 AGENT FETCHER
# =========================================================

def get_agent(agent_name):

    return AGENT_REGISTRY.get(agent_name)

# =========================================================
# 🔥 AGENT LIST
# =========================================================

def list_registered_agents():

    return list(
        AGENT_REGISTRY.keys()
    )
