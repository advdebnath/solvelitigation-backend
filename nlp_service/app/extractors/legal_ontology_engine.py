def classify_concepts(concepts):

    results = []

    for item in concepts:

        concept = item["concept"]

        label = "General"

        if any(
            x in concept.lower()
            for x in [
                "wage",
                "service",
                "employment",
                "employee",
                "labour",
                "industrial"
            ]
        ):
            label = "Service"

        elif any(
            x in concept.lower()
            for x in [
                "bail",
                "conviction",
                "sentence",
                "accused",
                "prosecution"
            ]
        ):
            label = "Criminal"

        elif any(
            x in concept.lower()
            for x in [
                "contract",
                "tenancy",
                "property",
                "possession"
            ]
        ):
            label = "Civil"

        results.append({
            **item,
            "category": label
        })

    return results
