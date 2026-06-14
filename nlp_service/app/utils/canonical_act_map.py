import re

# =========================================================
# 🔥 CANONICAL ACT NORMALIZATION MAP
# =========================================================

CANONICAL_ACT_MAP = {
    # -----------------------------------------------------
    # IPC
    # -----------------------------------------------------
    "ipc": "Indian Penal Code, 1860",
    "i.p.c": "Indian Penal Code, 1860",
    "indian penal code": "Indian Penal Code, 1860",
    "indian penal code, 1860": "Indian Penal Code, 1860",
    # -----------------------------------------------------
    # CrPC
    # -----------------------------------------------------
    "crpc": "Code of Criminal Procedure, 1973",
    "cr.p.c": "Code of Criminal Procedure, 1973",
    "code of criminal procedure": "Code of Criminal Procedure, 1973",
    "code of criminal procedure, 1973": "Code of Criminal Procedure, 1973",
    # -----------------------------------------------------
    # Constitution
    # -----------------------------------------------------
    "constitution": "Constitution of India",
    "constitution of india": "Constitution of India",
    # -----------------------------------------------------
    # Evidence Act
    # -----------------------------------------------------
    "evidence act": "Indian Evidence Act, 1872",
    "indian evidence act": "Indian Evidence Act, 1872",
    "indian evidence act, 1872": "Indian Evidence Act, 1872",
    # -----------------------------------------------------
    # CPC
    # -----------------------------------------------------
    "cpc": "Code of Civil Procedure, 1908",
    "code of civil procedure": "Code of Civil Procedure, 1908",
    "code of civil procedure, 1908": "Code of Civil Procedure, 1908",
    # -----------------------------------------------------
    # NI Act
    # -----------------------------------------------------
    "ni act": "Negotiable Instruments Act, 1881",
    "negotiable instruments act": "Negotiable Instruments Act, 1881",
    "negotiable instruments act, 1881": "Negotiable Instruments Act, 1881",
    # -----------------------------------------------------
    # NDPS
    # -----------------------------------------------------
    "ndps": "Narcotic Drugs and Psychotropic Substances Act, 1985",
    "ndps act": "Narcotic Drugs and Psychotropic Substances Act, 1985",
    "narcotic drugs and psychotropic substances act": "Narcotic Drugs and Psychotropic Substances Act, 1985",
    # -----------------------------------------------------
    # POCSO
    # -----------------------------------------------------
    "pocso": "Protection of Children from Sexual Offences Act, 2012",
    "pocso act": "Protection of Children from Sexual Offences Act, 2012",
    # -----------------------------------------------------
    # Arbitration
    # -----------------------------------------------------
    "arbitration act": "Arbitration and Conciliation Act, 1996",
    "arbitration and conciliation act": "Arbitration and Conciliation Act, 1996",
    "arbitration and conciliation act, 1996": "Arbitration and Conciliation Act, 1996",
}


# =========================================================
# 🔥 NORMALIZER
# =========================================================


def canonicalize_act_name(value):

    if not value:

        return value

    value = str(value).strip()

    value = re.sub(
        r'^(the|under the|of the)\s+',
        '',
        value,
        flags=re.I
    )

    value = re.sub(
        r'\s+',
        ' ',
        value
    )

    cleaned = value.lower()

    cleaned = cleaned.replace(".", "")

    cleaned = " ".join(cleaned.split())

    return CANONICAL_ACT_MAP.get(
        cleaned,
        value
    )
