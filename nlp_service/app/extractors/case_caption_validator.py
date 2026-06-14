import re


def validate_case_caption(case_number):

    if not case_number:
        return False

    case_number = str(case_number).strip()

    if not re.search(r"\d", case_number):
        return False

    invalid_patterns = [
        r"PETITIONER",
        r"RESPONDENT",
        r"ADVOCATE",
        r"COUNSEL",
    ]

    for pattern in invalid_patterns:

        if re.search(pattern, case_number, re.I):
            return False

    return True
