# =========================================================
# 🔥 MASTER JURISPRUDENTIAL INTELLIGENCE ORCHESTRATOR
# =========================================================

from app.core_intelligence.doctrine_evolution_graph import \
    build_doctrine_evolution
from app.core_intelligence.entity_resolution_engine import resolve_entities
from app.core_intelligence.judge_philosophy_engine import \
    build_judge_philosophy_profile
from app.core_intelligence.litigation_lineage_engine import \
    build_litigation_lineage
from app.core_intelligence.precedent_graph_engine import build_precedent_graph
from app.core_intelligence.predictive_outcome_engine import \
    predict_case_outcome
from app.core_intelligence.semantic_argument_engine import \
    generate_semantic_argument

# =========================================================
# 🔥 SAFE ORCHESTRATOR
# =========================================================


def run_full_jurisprudential_intelligence(current_case, historical_cases):

    intelligence = {
        "entity_resolution": None,
        "litigation_lineage": None,
        "precedent_graph": None,
        "doctrine_evolution": None,
        "judge_philosophy": None,
        "semantic_argument": None,
        "predictive_outcome": None,
    }

    # =====================================================
    # 🔥 ENTITY RESOLUTION
    # =====================================================

    try:

        petitioner = current_case.get("petitioner", "")

        intelligence["entity_resolution"] = resolve_entities(petitioner, petitioner)

    except Exception as e:

        intelligence["entity_resolution_error"] = str(e)

    # =====================================================
    # 🔥 LITIGATION LINEAGE
    # =====================================================

    try:

        intelligence["litigation_lineage"] = build_litigation_lineage(
            canonical_entity=current_case.get("petitioner", ""),
            entity_hash="AUTO",
            judgments=historical_cases,
        )

    except Exception as e:

        intelligence["litigation_lineage_error"] = str(e)

    # =====================================================
    # 🔥 PRECEDENT GRAPH
    # =====================================================

    try:

        precedent_graph = build_precedent_graph(
            source_case=current_case, candidate_cases=historical_cases
        )

        intelligence["precedent_graph"] = precedent_graph

    except Exception as e:

        precedent_graph = {}

        intelligence["precedent_graph_error"] = str(e)

    # =====================================================
    # 🔥 DOCTRINE EVOLUTION
    # =====================================================

    try:

        doctrine_data = build_doctrine_evolution(
            doctrine_name=current_case.get("issue", "UNKNOWN"),
            judgments=historical_cases,
        )

        intelligence["doctrine_evolution"] = doctrine_data

    except Exception as e:

        doctrine_data = {}

        intelligence["doctrine_evolution_error"] = str(e)

    # =====================================================
    # 🔥 JUDGE PHILOSOPHY
    # =====================================================

    try:

        judicial_profile = build_judge_philosophy_profile(
            judge_name=current_case.get("judge", "UNKNOWN"), judgments=historical_cases
        )

        intelligence["judge_philosophy"] = judicial_profile

    except Exception as e:

        judicial_profile = {}

        intelligence["judge_philosophy_error"] = str(e)

    # =====================================================
    # 🔥 SEMANTIC ARGUMENT
    # =====================================================

    try:

        semantic_argument = generate_semantic_argument(
            issue=current_case.get("issue", ""),
            precedent_graph=precedent_graph,
            judicial_profile=judicial_profile,
        )

        intelligence["semantic_argument"] = semantic_argument

    except Exception as e:

        semantic_argument = {}

        intelligence["semantic_argument_error"] = str(e)

    # =====================================================
    # 🔥 PREDICTIVE OUTCOME
    # =====================================================

    try:

        intelligence["predictive_outcome"] = predict_case_outcome(
            issue=current_case.get("issue", ""),
            doctrine_data=doctrine_data,
            judicial_profile=judicial_profile,
            precedent_graph=precedent_graph,
        )

    except Exception as e:

        intelligence["predictive_outcome_error"] = str(e)

    return intelligence


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    current_case = {
        "petitioner": "BHAGWAN DASS",
        "issue": "REINSTATEMENT",
        "judge": "Justice Chandrachud",
        "category": "SERVICE LAW",
        "actNames": ["CONSTITUTION OF INDIA"],
        "pointsOfLaw": ["REINSTATEMENT"],
    }

    historical_cases = [
        {
            "caseNumber": "2024 SLSC 101",
            "category": "SERVICE LAW",
            "actNames": ["CONSTITUTION OF INDIA"],
            "pointsOfLaw": ["REINSTATEMENT"],
            "judges": ["Justice Chandrachud"],
            "ratio": (
                "Constitutional morality "
                "and procedural fairness "
                "require reinstatement."
            ),
            "confidence": 82,
        },
        {
            "caseNumber": "2018 SLSC 55",
            "category": "SERVICE LAW",
            "actNames": ["CONSTITUTION OF INDIA"],
            "pointsOfLaw": ["NATURAL JUSTICE"],
            "judges": ["Justice Rao"],
            "ratio": ("Beneficial interpretation " "supports employee rights."),
            "confidence": 78,
        },
    ]

    result = run_full_jurisprudential_intelligence(
        current_case=current_case, historical_cases=historical_cases
    )

    print(result)
