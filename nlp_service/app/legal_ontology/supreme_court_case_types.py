import re

# =========================================================
# 🔥 SUPREME COURT CASE TYPE ONTOLOGY
# =========================================================

SUPREME_COURT_CASE_TYPES = {

    "CIVIL_APPEAL": {
        "display": "Civil Appeal",
        "family": "APPEAL",
        "category": "CIVIL",
        "patterns": [
            r"\bCIVIL\s+APPEAL\b",
            r"\bC\.?\s*A\.?\b",
        ]
    },

    "CRIMINAL_APPEAL": {
        "display": "Criminal Appeal",
        "family": "APPEAL",
        "category": "CRIMINAL",
        "patterns": [
            r"\bCRIMINAL\s+APPEAL\b",
            r"\bCRL\.?\s*A\.?\b",
        ]
    },

    "WRIT_PETITION_CIVIL": {
        "display": "Writ Petition (Civil)",
        "family": "PETITION",
        "category": "CIVIL",
        "patterns": [
            r"\bWRIT\s+PETITION\s*\(?\s*C(?:IVIL)?\s*\)?",
            r"\bW\.?\s*P\.?\s*\(C\)",
            r"\bWP\s*\(C\)"
        ]
    },

    "WRIT_PETITION_CRIMINAL": {
        "display": "Writ Petition (Criminal)",
        "family": "PETITION",
        "category": "CRIMINAL",
        "patterns": [
            r"\bWRIT\s+PETITION\s*\(?\s*CRL",
            r"\bW\.?\s*P\.?\s*\(CRL",
            r"\bWP\s*\(CRL"
        ]
    },

    "SPECIAL_LEAVE_PETITION_CIVIL": {
        "display": "Special Leave Petition (Civil)",
        "family": "PETITION",
        "category": "CIVIL",
        "patterns": [
            r"\bSPECIAL\s+LEAVE\s+PETITION\s*\(?\s*C",
            r"\bSLP\s*\(C\)",
            r"\bS\.?\s*L\.?\s*P\.?\s*\(C\)"
        ]
    },

    "SPECIAL_LEAVE_PETITION_CRIMINAL": {
        "display": "Special Leave Petition (Criminal)",
        "family": "PETITION",
        "category": "CRIMINAL",
        "patterns": [
            r"\bSPECIAL\s+LEAVE\s+PETITION\s*\(?\s*CRL",
            r"\bSLP\s*\(CRL",
            r"\bS\.?\s*L\.?\s*P\.?\s*\(CRL"
        ]
    },

    "REVIEW_PETITION": {
        "display": "Review Petition",
        "family": "PETITION",
        "category": "CIVIL",
        "patterns": [
            r"\bREVIEW\s+PETITION\b"
        ]
    },

    "CURATIVE_PETITION": {
        "display": "Curative Petition",
        "family": "PETITION",
        "category": "CIVIL",
        "patterns": [
            r"\bCURATIVE\s+PETITION\b"
        ]
    },

    "TRANSFER_PETITION_CIVIL": {
        "display": "Transfer Petition (Civil)",
        "family": "TRANSFER",
        "category": "CIVIL",
        "patterns": [
            r"\bTRANSFER\s+PETITION\s*\(?\s*C",
            r"\bT\.?\s*P\.?\s*\(C\)"
        ]
    },

    "TRANSFER_PETITION_CRIMINAL": {
        "display": "Transfer Petition (Criminal)",
        "family": "TRANSFER",
        "category": "CRIMINAL",
        "patterns": [
            r"\bTRANSFER\s+PETITION\s*\(?\s*CRL",
            r"\bT\.?\s*P\.?\s*\(CRL"
        ]
    },

    "CONTEMPT_PETITION_CIVIL": {
        "display": "Contempt Petition (Civil)",
        "family": "CONTEMPT",
        "category": "CIVIL",
        "patterns": [
            r"\bCONTEMPT\s+PETITION\s*\(?\s*C",
            r"\bCONMT\.?\s*PET\.?\s*\(C\)"
        ]
    },

    "CONTEMPT_PETITION_CRIMINAL": {
        "display": "Contempt Petition (Criminal)",
        "family": "CONTEMPT",
        "category": "CRIMINAL",
        "patterns": [
            r"\bCONTEMPT\s+PETITION\s*\(?\s*CRL",
            r"\bCONMT\.?\s*PET\.?\s*\(CRL"
        ]
    },

    "ARBITRATION_PETITION": {
        "display": "Arbitration Petition",
        "family": "ARBITRATION",
        "category": "CIVIL",
        "patterns": [
            r"\bARBITRATION\s+PETITION\b"
        ]
    },

    "ELECTION_PETITION": {
        "display": "Election Petition",
        "family": "ELECTION",
        "category": "CIVIL",
        "patterns": [
            r"\bELECTION\s+PETITION\b"
        ]
    },

    "DIARY_MATTER": {
        "display": "Diary Matter",
        "family": "DIARY",
        "category": "UNCLASSIFIED",
        "patterns": [
            r"\bDIARY\s+NO",
            r"\bD\.?\s*NO\.?"
        ]
    },

    "ORIGINAL_SUIT": {
        "display": "Original Suit",
        "family": "ORIGINAL",
        "category": "CIVIL",
        "patterns": [
            r"\bORIGINAL\s+SUIT\b"
        ]
    },

    "SUO_MOTU_WRIT": {
        "display": "Suo Motu Writ Petition",
        "family": "SUO_MOTU",
        "category": "CIVIL",
        "patterns": [
            r"\bSUO\s+MOTU\b",
            r"\bSMW\s*\(C\)"
        ]
    },

    "PIL": {
        "display": "Public Interest Litigation",
        "family": "PUBLIC_INTEREST",
        "category": "CIVIL",
        "patterns": [
            r"\bPUBLIC\s+INTEREST\s+LITIGATION\b",
            r"\bPIL\b"
        ]
    },
}

# =========================================================
# 🔥 CASE TYPE EXTRACTOR
# =========================================================

def detect_supreme_court_case_type(text):

    if not text:
        return {}

    normalized_text = re.sub(
        r"\s+",
        " ",
        str(text)
    ).upper()

    best_match = None
    best_score = 0

    for canonical, meta in SUPREME_COURT_CASE_TYPES.items():

        for pattern in meta.get("patterns", []):

            if re.search(
                pattern,
                normalized_text,
                re.IGNORECASE
            ):

                score = 90

                if "SUPREME COURT" in normalized_text:
                    score += 5

                if "JURISDICTION" in normalized_text:
                    score += 5

                if score > best_score:

                    best_score = score

                    best_match = {
                        "canonical": canonical,
                        "display": meta.get("display"),
                        "family": meta.get("family"),
                        "category": meta.get("category"),
                        "confidence": score,
                        "matched_pattern": pattern
                    }

    return best_match or {}
