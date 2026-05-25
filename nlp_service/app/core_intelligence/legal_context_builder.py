from typing import Dict, List


def build_validated_legal_context(
    canonical_acts: List[str],
    resolved_sections: List[dict],
    canonical_issue_data: dict,
    court_type: str = "",
    case_type: str = ""
) -> Dict:

    domain = "UNKNOWN"

    joined_acts = " ".join(canonical_acts).lower()

    # =====================================================
    # 🔥 DOMAIN RESOLUTION ENGINE
    # =====================================================

    if "income tax" in joined_acts:
        domain = "TAXATION"

    elif "goods and services tax" in joined_acts:
        domain = "TAXATION"

    elif "companies act" in joined_acts:
        domain = "CORPORATE"

    elif "ndps" in joined_acts:
        domain = "CRIMINAL"

    elif "penal code" in joined_acts:
        domain = "CRIMINAL"

    elif "constitution" in joined_acts:
        domain = "CONSTITUTIONAL"

    elif "service" in joined_acts:
        domain = "SERVICE"

    # =====================================================
    # 🔥 VALIDATED ACT FIREWALL
    # =====================================================

    validated_acts = []

    rejected_acts = []

    for act in canonical_acts:

        lower_act = act.lower()

        if domain == "TAXATION":

            if (
                "criminal procedure" in lower_act
                or "penal code" in lower_act
                or "ndps" in lower_act
            ):
                rejected_acts.append(act)
                continue

        validated_acts.append(act)

    return {
        "domain": domain,
        "canonical_acts": validated_acts,
        "rejected_acts": rejected_acts,
        "resolved_sections": resolved_sections,
        "issues": canonical_issue_data,
        "validated": True
    }
