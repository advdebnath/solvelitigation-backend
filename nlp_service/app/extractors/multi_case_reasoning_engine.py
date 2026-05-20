import re


# =========================================================
# 🔥 CLEAN
# =========================================================

def clean_text(text):

    text = re.sub(
        r"\s+",
        " ",
        str(text)
    )

    return text.strip()


# =========================================================
# 🔥 BUILD CASE SUMMARY
# =========================================================

def build_case_summary(case):

    parts = []

    issue = case.get(
        "dominant_issue"
    )

    if issue:

        parts.append(
            f"Issue: {issue}"
        )

    holding = case.get(
        "final_holding"
    )

    if holding:

        parts.append(
            f"Holding: {holding}"
        )

    doctrine = case.get(
        "doctrine"
    )

    if doctrine:

        parts.append(
            f"Doctrine: {doctrine}"
        )

    return " | ".join(parts)


# =========================================================
# 🔥 GENERATE REASONING
# =========================================================

def generate_multi_case_reasoning(

    cases
):

    try:

        if not cases:

            return {

                "multi_case_reasoning":
                    "",

                "comparative_analysis": [],

                "confidence":
                    0
            }

        comparative = []

        doctrines = set()

        holdings = set()

        issues = set()

        # =================================================
        # 🔥 ANALYZE CASES
        # =================================================

        for case in cases:

            summary = build_case_summary(
                case
            )

            comparative.append(
                summary
            )

            doctrine = case.get(
                "doctrine"
            )

            if doctrine:

                doctrines.add(
                    doctrine
                )

            holding = case.get(
                "final_holding"
            )

            if holding:

                holdings.add(
                    holding
                )

            issue = case.get(
                "dominant_issue"
            )

            if issue:

                issues.add(
                    issue
                )

        # =================================================
        # 🔥 BUILD REASONING
        # =================================================

        reasoning_parts = []

        if doctrines:

            reasoning_parts.append(

                "The jurisprudence reflects evolving interpretation of doctrines such as "
                +
                ", ".join(list(doctrines)[:5])
                +
                "."
            )

        if holdings:

            reasoning_parts.append(

                "The courts adopted varying operative outcomes including "
                +
                ", ".join(list(holdings)[:5])
                +
                "."
            )

        if issues:

            reasoning_parts.append(

                "The disputes consistently revolved around issues involving "
                +
                ", ".join(list(issues)[:5])
                +
                "."
            )

        reasoning_parts.append(

            "Comparative reasoning indicates gradual doctrinal refinement across multiple judgments."
        )

        # =================================================
        # 🔥 FINAL
        # =================================================

        reasoning = " ".join(
            reasoning_parts
        )

        reasoning = clean_text(
            reasoning
        )

        result = {

            "multi_case_reasoning":
                reasoning,

            "comparative_analysis":
                comparative,

            "confidence":
                95
        }

        print(
            "✅ Multi-Case Reasoning Generated:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Multi-Case Reasoning Error:",
            str(e)
        )

        return {

            "multi_case_reasoning":
                "",

            "comparative_analysis": [],

            "confidence":
                0
        }


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample_cases = [

        {

            "dominant_issue":
                "Natural Justice",

            "final_holding":
                "Appeal Allowed",

            "doctrine":
                "procedural fairness"
        },

        {

            "dominant_issue":
                "Constitutional Due Process",

            "final_holding":
                "High Court Set Aside",

            "doctrine":
                "due process"
        }
    ]

    print(

        generate_multi_case_reasoning(

            sample_cases
        )
    )
