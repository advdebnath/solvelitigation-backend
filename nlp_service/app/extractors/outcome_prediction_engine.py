import re


# =========================================================
# 🔥 POSITIVE FACTORS
# =========================================================

POSITIVE_FACTORS = [

    r"appeal\s+(is\s+)?allowed",

    r"petition\s+(is\s+)?allowed",

    r"submission\s+(deserves\s+)?acceptance",

    r"natural\s+justice\s+was\s+violated",

    r"high\s+court.*set\s+aside",

    r"tribunal\s+(is\s+)?restored",

    r"argument\s+(is\s+)?accepted",

    r"constitutional\s+violation",

    r"burden\s+not\s+discharged"
]


# =========================================================
# 🔥 NEGATIVE FACTORS
# =========================================================

NEGATIVE_FACTORS = [

    r"appeal\s+(is\s+)?dismissed",

    r"petition\s+(is\s+)?dismissed",

    r"submission\s+(is\s+)?rejected",

    r"argument\s+(is\s+)?rejected",

    r"without\s+merit",

    r"conviction\s+upheld",

    r"sentence\s+affirmed",

    r"claim\s+rejected"
]


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
# 🔥 DETECT FACTORS
# =========================================================

def detect_factors(text, patterns):

    findings = []

    for pattern in patterns:

        matches = re.finditer(
            pattern,
            text,
            re.I
        )

        for match in matches:

            value = clean_text(
                match.group(0)
            )

            if value not in findings:

                findings.append(value)

    return findings


# =========================================================
# 🔥 PREDICT OUTCOME
# =========================================================

def predict_outcome(text):

    try:

        text = clean_text(text)

        # =================================================
        # 🔥 POSITIVE
        # =================================================

        positive = detect_factors(
            text,
            POSITIVE_FACTORS
        )

        # =================================================
        # 🔥 NEGATIVE
        # =================================================

        negative = detect_factors(
            text,
            NEGATIVE_FACTORS
        )

        # =================================================
        # 🔥 SCORE
        # =================================================

        score = (

            len(positive) * 15

            -

            len(negative) * 12
        )

        # =================================================
        # 🔥 OUTCOME
        # =================================================

        if score >= 40:

            outcome = "Appeal Likely Allowed"

        elif score >= 15:

            outcome = "Petitioner Likely to Succeed"

        elif score <= -40:

            outcome = "Appeal Likely Dismissed"

        elif score <= -15:

            outcome = "Respondent Likely to Succeed"

        else:

            outcome = "Outcome Uncertain"

        # =================================================
        # 🔥 CONFIDENCE
        # =================================================

        confidence = min(

            55 + abs(score),

            95
        )

        # =================================================
        # 🔥 SUPPORTING FACTORS
        # =================================================

        supporting = []

        supporting.extend(
            positive[:5]
        )

        supporting.extend(
            negative[:5]
        )

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {

            "predicted_outcome":
                outcome,

            "confidence":
                confidence,

            "positive_factors":
                positive,

            "negative_factors":
                negative,

            "supporting_factors":
                supporting
        }

        print(
            "✅ Outcome Prediction:"
        )

        print(result)

        return result

    except Exception as e:

        print(
            "❌ Outcome Prediction Error:",
            str(e)
        )

        return {

            "predicted_outcome":
                "Unknown",

            "confidence":
                0
        }


# =========================================================
# 🔥 HYBRID JURISPRUDENTIAL PREDICTION
# =========================================================

def predict_jurisprudential_outcome(

    full_text="",
    dominant_issue=None,
    ratio_issue_fusion=None,
    operative_data=None
):

    base_prediction = predict_outcome(
        full_text
    )

    issue_name = None

    # -----------------------------------------------------
    # DOMINANT ISSUE
    # -----------------------------------------------------

    if isinstance(dominant_issue, dict):

        issue_name = dominant_issue.get(
            "dominant_issue"
        )

    # -----------------------------------------------------
    # FUSION FALLBACK
    # -----------------------------------------------------

    if not issue_name:

        if isinstance(
            ratio_issue_fusion,
            dict
        ):

            issue_name = (
                ratio_issue_fusion.get(
                    "dominant_issue"
                )
            )

    # -----------------------------------------------------
    # ISSUE BOOSTING
    # -----------------------------------------------------

    if issue_name:

        base_prediction[
            "dominant_issue"
        ] = issue_name

        # FIR QUASHING
        if issue_name == "FIR Quashing":

            base_prediction[
                "prediction_context"
            ] = (
                "Settlement and abuse-of-process principles often influence quashing outcomes."
            )

        # CHEQUE DISHONOUR
        elif issue_name == "Cheque Dishonour":

            base_prediction[
                "prediction_context"
            ] = (
                "Cheque dishonour litigation commonly depends on signature admission and legally enforceable debt."
            )

        # HOMICIDE
        elif issue_name == "Homicide":

            base_prediction[
                "prediction_context"
            ] = (
                "Homicide outcomes heavily depend on eyewitness credibility and forensic corroboration."
            )

        # DOWRY DEATH
        elif issue_name == "Dowry Death":

            base_prediction[
                "prediction_context"
            ] = (
                "Cruelty proximate to death significantly affects dowry death adjudication."
            )

    # -----------------------------------------------------
    # OPERATIVE BOOST
    # -----------------------------------------------------

    if isinstance(operative_data, dict):

        holding = str(

            operative_data.get(
                "final_holding",
                ""
            )

        ).lower()

        if "dismissed" in holding:

            base_prediction[
                "confidence"
            ] += 5

        if "allowed" in holding:

            base_prediction[
                "confidence"
            ] += 5

    # -----------------------------------------------------
    # FINAL CAP
    # -----------------------------------------------------

    base_prediction[
        "confidence"
    ] = min(

        95,

        base_prediction.get(
            "confidence",
            0
        )
    )

    print(
        "✅ Hybrid Jurisprudential Prediction:"
    )

    print(base_prediction)

    return base_prediction


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    The appeal is allowed.

    The High Court judgment is set aside.

    The Tribunal is restored.

    The petitioner submission deserves acceptance.

    Natural justice was violated.
    """

    print(
        predict_outcome(sample)
    )

    print(
        predict_jurisprudential_outcome(
            full_text=sample,
            dominant_issue={
                "dominant_issue": "Writ Jurisdiction"
            },
            ratio_issue_fusion={
                "dominant_issue": "Writ Jurisdiction"
            },
            operative_data={
                "final_holding": "Appeal Allowed"
            }
        )
    )
