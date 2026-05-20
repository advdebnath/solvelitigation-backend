import re


CANONICAL_POINT_MAP = {

    "Equal Pay For Equal Work": [
        "equal pay",
        "pay parity",
        "revised pay scale",
        "salary discrimination"
    ],

    "Departmental Proceeding": [
        "disciplinary enquiry",
        "departmental enquiry",
        "charge memo",
        "service misconduct"
    ],

    "Quashing Of FIR": [
        "fir quashed",
        "criminal proceedings quashed",
        "section 482",
        "quash criminal proceedings"
    ],

    "Anticipatory Bail": [
        "pre-arrest bail",
        "anticipatory bail application"
    ]
}


def normalize_points(points):

    if not isinstance(points, list):
        return []

    normalized = []

    seen = set()

    for point_data in points:

        if not isinstance(point_data, dict):
            continue

        raw_point = str(
            point_data.get(
                "point",
                ""
            )
        ).strip()

        raw_lower = raw_point.lower()

        canonical_point = raw_point

        aliases = []

        for canonical, alias_list in CANONICAL_POINT_MAP.items():

            matched = False

            for alias in alias_list:

                alias_lower = alias.lower()

                if (
                    alias_lower in raw_lower
                    or raw_lower in alias_lower
                ):

                    canonical_point = canonical

                    aliases.append(raw_point)

                    matched = True

                    break

            if matched:
                break

        unique_key = (
            canonical_point.lower(),
            point_data.get("category", "")
        )

        if unique_key in seen:
            continue

        seen.add(unique_key)

        normalized.append({

            "point": canonical_point,

            "category": point_data.get(
                "category",
                "General"
            ),

            "score": point_data.get(
                "score",
                0
            ),

            "aliases": aliases,

            "canonical": True
        })

    return normalized
