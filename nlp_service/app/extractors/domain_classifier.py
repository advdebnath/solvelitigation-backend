import re


DOMAIN_PATTERNS = {

    "Service Law": [
        r"\bequal\\s+pay\\s+for\\s+equal\\s+work\\b",
        r"\bpay\\s+parity\\b",
        r"\bdepartmental\\s+proceeding\\b",
        r"\bdisciplinary\\b",
        r"\bservice\\s+rules\\b",
        r"\breinstatement\\b",
        r"\bpromotion\\b",
        r"\bpay\\s+scale\\b",
        r"\bemployees?\\b",
        r"\bemployee\\s+benefits\\b",
        r"\bservice\\s+benefits\\b",
        r"\brevised\\s+pay\\s+scale\\b",
        r"\bpay\\s+revision\\b",
        r"\bpay\\s+commission\\b",
        r"\bcounterparts\\b",
        r"\bregularization\\b",
        r"\bfederation\\s+employees\\b",
        r"\bretiral\\s+benefits\\b",
        r"\bgovernment\\s+servant\\b",
    ],

    "Taxation Law": [
        r"\bincome\\s+tax\\b",
        r"\bgst\\b",
        r"\bvat\\b",
        r"\binput\\s+tax\\s+credit\\b",
        r"\bassessment\\b",
        r"\bexcise\\b",
        r"\bcustoms\\b",
    ],

    "Corporate Law": [
        r"\bcompanies\\s+act\\b",
        r"\bshareholder\\b",
        r"\bboard\\s+of\\s+directors\\b",
        r"\binsolvency\\b",
        r"\bnclt\\b",
        r"\bsebi\\b",
    ],

    "Constitutional Law": [
        r"\barticle\\s+14\\b",
        r"\barticle\\s+21\\b",
        r"\bwrit\\s+petition\\b",
        r"\bconstitutional\\b",
        r"\bjudicial\\s+review\\b",
    ],

    "Property Law": [
        r"\bproperty\\b",
        r"\btitle\\b",
        r"\bownership\\b",
        r"\bpossession\\b",
        r"\bpartition\\b",
    ]
}


def classify_domain(
    full_text="",
    points_of_law=None
):

    if not full_text:

        return {
            "domain": "Unknown",
            "confidence": 0
        }


    print("🔥 RAW POINTS INPUT TYPE:")
    print(type(points_of_law))
    print(points_of_law)

    if points_of_law is None:
        points_of_law = []

    text = full_text.lower()

    scores = {}

    for domain, patterns in DOMAIN_PATTERNS.items():

        score = 0

        for pattern in patterns:

            matches = re.findall(
                pattern,
                text,
                flags=re.I
            )

            score += len(matches)

        scores[domain] = score

    # =====================================================
    # 🔥 POINT-OF-LAW DOMAIN BOOST
    # =====================================================


    print("✅ DOMAIN BOOST INPUT:")
    print(points_of_law)

    for point in points_of_law:

        if not isinstance(point, dict):
            continue

        point_category = point.get(
            "category",
            ""
        )

        if point_category == "Service":
            scores["Service Law"] += 50

        elif point_category == "Taxation":
            scores["Taxation Law"] += 50

        elif point_category == "Corporate":
            scores["Corporate Law"] += 50

        elif point_category == "Constitutional":
            scores["Constitutional Law"] += 30

    best_domain = max(
        scores,
        key=scores.get
    )

    if scores[best_domain] <= 0:

        return {
            "domain": "General Civil",
            "confidence": 10,
            "scores": scores
        }

    return {
        "domain": best_domain,
        "confidence": min(
            95,
            50 + scores[best_domain] * 5
        ),
        "scores": scores
    }
