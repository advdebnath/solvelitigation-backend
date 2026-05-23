from collections import defaultdict


# =========================================================
# 🔥 BUILD LITIGATION LINEAGE
# =========================================================

def build_litigation_lineage(

    canonical_entity,

    entity_hash,

    judgments
):

    lineage = {

        "party": canonical_entity,

        "entity_hash": entity_hash,

        "cases_found": 0,

        "courts": set(),

        "roles": set(),

        "legal_domains": set(),

        "judges": set(),

        "case_numbers": [],

        "litigation_profile": {

            "repeat_litigant": False,

            "government_entity": False,

            "risk_level": "LOW"
        }
    }

    if not judgments:
        return lineage

    for doc in judgments:

        lineage["cases_found"] += 1

        court = doc.get(
            "court",
            ""
        )

        if court:
            lineage["courts"].add(court)

        role = doc.get(
            "partyRole",
            ""
        )

        if role:
            lineage["roles"].add(role)

        category = doc.get(
            "category",
            ""
        )

        if category:
            lineage["legal_domains"].add(
                category
            )

        case_number = doc.get(
            "caseNumber",
            ""
        )

        if case_number:
            lineage["case_numbers"].append(
                case_number
            )

        judges = doc.get(
            "judges",
            []
        )

        if isinstance(judges, list):

            for judge in judges:

                if judge:
                    lineage["judges"].add(
                        str(judge)
                    )

    # -----------------------------------------------------
    # 🔥 GOVERNMENT DETECTION
    # -----------------------------------------------------

    upper = canonical_entity.upper()

    if (
        "UNION OF INDIA" in upper
        or "STATE OF" in upper
        or "COMMISSIONER" in upper
        or "DEPARTMENT" in upper
        or "MINISTRY" in upper
    ):

        lineage["litigation_profile"][
            "government_entity"
        ] = True

    # -----------------------------------------------------
    # 🔥 REPEAT LITIGANT
    # -----------------------------------------------------

    if lineage["cases_found"] >= 3:

        lineage["litigation_profile"][
            "repeat_litigant"
        ] = True

    # -----------------------------------------------------
    # 🔥 RISK LEVEL
    # -----------------------------------------------------

    if lineage["cases_found"] >= 20:

        lineage["litigation_profile"][
            "risk_level"
        ] = "HIGH"

    elif lineage["cases_found"] >= 5:

        lineage["litigation_profile"][
            "risk_level"
        ] = "MODERATE"

    # -----------------------------------------------------
    # 🔥 SERIALIZATION
    # -----------------------------------------------------

    lineage["courts"] = list(
        lineage["courts"]
    )

    lineage["roles"] = list(
        lineage["roles"]
    )

    lineage["legal_domains"] = list(
        lineage["legal_domains"]
    )

    lineage["judges"] = list(
        lineage["judges"]
    )

    return lineage


# =========================================================
# 🔥 TEST MODE
# =========================================================

if __name__ == "__main__":

    sample_judgments = [

        {
            "court": "SUPREME COURT OF INDIA",

            "partyRole": "RESPONDENT",

            "category": "SERVICE LAW",

            "caseNumber": "2024 SLSC 101",

            "judges": [
                "Justice Chandrachud"
            ]
        },

        {
            "court": "DELHI HIGH COURT",

            "partyRole": "APPELLANT",

            "category": "TAXATION",

            "caseNumber": "2023 SLHC_DEL 88",

            "judges": [
                "Justice Rao"
            ]
        }
    ]

    result = build_litigation_lineage(

        canonical_entity="UNION OF INDIA",

        entity_hash="538ee12bfc58",

        judgments=sample_judgments
    )

    print(result)
