from app.db.mongo import get_db


def detect_dynamic_issue(full_text=""):

    result = {
        "dominant_issue": None,
        "confidence": 0,
        "source": "dynamic"
    }

    if not full_text:
        return result

    try:

        db = get_db()

        text = full_text.lower()

        patterns = list(
            db.issuePatterns.find(
                {"active": True}
            )
        )

        best_score = 0

        for item in patterns:

            score = 0

            for keyword in item.get(
                "keywords",
                []
            ):

                if keyword.lower() in text:

                    score += item.get(
                        "weight",
                        10
                    )

            if score > best_score:

                best_score = score

                result = {
                    "dominant_issue":
                        item.get("issue"),
                    "confidence":
                        min(score, 95),
                    "source":
                        "dynamic"
                }

        return result

    except Exception as e:

        print(
            "❌ DYNAMIC ISSUE ENGINE ERROR:",
            str(e)
        )

        return result
