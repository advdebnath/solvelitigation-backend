import re


# =========================================================
# 🔥 TOKENIZER
# =========================================================

def tokenize(text):

    return set(
        re.findall(
            r'[a-zA-Z]+',
            str(text).lower()
        )
    )


# =========================================================
# 🔥 SEMANTIC OVERLAP
# =========================================================

def semantic_overlap(a, b):

    ta = tokenize(a)
    tb = tokenize(b)

    if not ta or not tb:
        return 0

    overlap = ta.intersection(tb)

    return int(
        (
            len(overlap)
            / max(len(ta), 1)
        ) * 100
    )


# =========================================================
# 🔥 LINK POINTS ↔ RATIO
# =========================================================

def link_points_with_ratio(
    points_of_law,
    ratio_data
):

    if not isinstance(points_of_law, list):
        return points_of_law

    candidates = ratio_data.get(
        "candidates",
        []
    )

    enriched = []

    for point in points_of_law:

        if not isinstance(point, dict):

            enriched.append(point)
            continue

        point_name = str(
            point.get(
                "point",
                ""
            )
        )

        best_candidate = None
        best_score = 0

        for candidate in candidates:

            candidate_text = str(
                candidate.get(
                    "text",
                    ""
                )
            )

            overlap = semantic_overlap(
                point_name,
                candidate_text
            )

            score = (
                overlap
                +
                int(
                    candidate.get(
                        "score",
                        0
                    )
                )
            )

            if score > best_score:

                best_score = score
                best_candidate = candidate

        if best_candidate:

            point["ratio_support"] = {

                "text":
                    best_candidate.get(
                        "text",
                        ""
                    )[:1200],

                "confidence":
                    min(
                        95,
                        best_score
                    ),

                "source":
                    best_candidate.get(
                        "source",
                        "paragraph"
                    ),

                "chunk_type":
                    best_candidate.get(
                        "chunk_type",
                        "UNKNOWN"
                    )
            }

        enriched.append(point)

    return enriched


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    points = [
        {
            "point": "Article 32 Remedy"
        }
    ]

    ratio = {
        "candidates": [
            {
                "text":
                    "Article 32 empowers this Court "
                    "to enforce constitutional remedies.",

                "score": 88,

                "chunk_type":
                    "RATIO_DECIDENDI"
            }
        ]
    }

    print(
        link_points_with_ratio(
            points,
            ratio
        )
    )
