import re

# =========================================================
# 🔥 TEXT NORMALIZATION
# =========================================================


def normalize(text):

    if not text:
        return ""

    text = str(text).lower()

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 LOCAL EVIDENTIARY CHECK
# =========================================================


def locally_supported(term, full_text):

    term = normalize(term)

    text = normalize(full_text)

    if not term or not text:
        return False

    if term in text:
        return True

    words = term.split()

    matched = 0

    for word in words:

        if len(word) <= 3:
            continue

        if word in text:
            matched += 1

    if matched >= max(1, len(words) // 2):
        return True

    return False


# =========================================================
# 🔥 ACT VALIDATION
# =========================================================


def validate_acts(acts, full_text):

    validated = []

    CRIMINAL_CORE_ACTS = {
        "Indian Penal Code, 1860",
        "Code Of Criminal Procedure, 1973",
        "Narcotic Drugs And Psychotropic Substances Act, 1985",
        "Indian Evidence Act, 1872",
    }

    for act in acts:

        # =========================================
        # 🔥 CRIMINAL CORE OVERRIDE
        # =========================================

        if act in CRIMINAL_CORE_ACTS:

            validated.append(act)

            continue

        # =========================================
        # 🔥 OCR-TOLERANT VALIDATION
        # =========================================

        if locally_supported(act, full_text):

            validated.append(act)

        else:

            print("❌ REJECTED ACT:", act)

    return validated


# =========================================================
# 🔥 POINT OF LAW VALIDATION
# =========================================================


def validate_points(points, full_text):

    validated = []

    for item in points:

        point = ""

        if isinstance(item, dict):

            point = item.get("point", "")

        else:

            point = str(item)

        if locally_supported(point, full_text):

            validated.append(item)

        else:

            print("❌ REJECTED POINT:", point)

    return validated


# =========================================================
# 🔥 ISSUE VALIDATION
# =========================================================


def validate_issue(issue_data, full_text):

    if not isinstance(issue_data, dict):
        return issue_data

    dominant_issue = issue_data.get("dominant_issue", "")

    if not locally_supported(dominant_issue, full_text):

        print("❌ REJECTED ISSUE:", dominant_issue)

        issue_data["dominant_issue"] = "General"

        issue_data["confidence"] = 20

    return issue_data
