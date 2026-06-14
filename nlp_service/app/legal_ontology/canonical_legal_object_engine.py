import re

# =========================================================
# 🔒 CANONICAL LEGAL OBJECT ENGINE
# =========================================================

CANONICAL_ACT_MAP = {
    "ipc": "Indian Penal Code, 1860",
    "indian penal code": "Indian Penal Code, 1860",
    "crpc": "Code of Criminal Procedure, 1973",
    "code of criminal procedure": "Code of Criminal Procedure, 1973",
    "constitution": "Constitution Of India",
    "constitution of india": "Constitution Of India",
    "ndps": "NDPS Act",
    "ndps act": "NDPS Act",
}

CANONICAL_POINT_MAP = {
    "quashing of fir": "Quashing Of FIR",
    "fir quashed": "Quashing Of FIR",
    "anticipatory bail": "Anticipatory Bail",
    "bail granted": "Grant Of Bail",
    "departmental proceeding": "Departmental Proceeding",
    "reinstatement": "Service Reinstatement",
}

# =========================================================
# 🔒 ACT CANONICALIZATION
# =========================================================


def canonicalize_act_name(act):

    if not act:
        return None

    act = str(act).strip()

    act = re.sub(
        r'^(the|under the|of the)\s+',
        '',
        act,
        flags=re.I
    )

    act = re.sub(
        r'\s+',
        ' ',
        act
    )

    normalized = act.lower()

    return CANONICAL_ACT_MAP.get(
        normalized,
        act
    )


# =========================================================
# 🔒 POINT OF LAW CANONICALIZATION
# =========================================================


def canonicalize_point_of_law(point):

    if not point:
        return None

    normalized = re.sub(r"\s+", " ", str(point).strip().lower())

    return CANONICAL_POINT_MAP.get(normalized, str(point).strip())


# =========================================================
# 🔒 IMMUTABLE LEGAL OBJECT
# =========================================================


def build_canonical_legal_object(label, object_type):

    if not label:
        return None

    label = str(label).strip()

    canonical_id = f"{object_type.upper()}::{label}"

    return {"id": canonical_id, "label": label, "type": object_type.upper()}
