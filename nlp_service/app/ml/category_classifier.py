def classify_category(acts, text):
    text = (text or "").upper()

    # =========================================
    # 🔥 PRIORITY 1 — CRIMINAL (STRICT)
    # =========================================
    criminal_patterns = [
        "CRIMINAL APPEAL",
        "CRL.",
        "CRIMINAL",
        "IPC",
        "CRPC",
        "NDPS",
        "POCSO",
        "FIR",
        "BAIL",
    ]

    if any(p in text for p in criminal_patterns):
        return "Criminal"

    # =========================================
    # 🔥 PRIORITY 2 — CIVIL (STRICT)
    # =========================================
    civil_patterns = [
        "CIVIL APPEAL",
        "SLP (C)",
        "SLP(C)",
        "SLP (CIVIL)",
        "WRIT PETITION (CIVIL)",
        "WRIT (C)",
        "CPC",
        "CONTRACT",
        "ARBITRATION",
        "SUIT",
    ]

    if any(p in text for p in civil_patterns):
        return "Civil"

    # =========================================
    # 🔥 PRIORITY 3 — SERVICE LAW
    # =========================================
    service_patterns = [
        "SERVICE",
        "DEPARTMENTAL",
        "DISCIPLINARY",
        "TERMINATION",
        "DISMISSAL",
        "REINSTATEMENT",
        "PROMOTION",
        "GOVERNMENT SERVANT",
        "SERVICE TRIBUNAL",
        "APPOINTMENT",
    ]

    if any(p in text for p in service_patterns):
        return "Service"

    # =========================================
    # 🔥 PRIORITY 4 — TAXATION / CORPORATE
    # =========================================
    tax_patterns = [
        "INCOME TAX",
        "GST",
        "VAT",
        "CUSTOMS",
        "EXCISE",
        "ASSESSMENT",
        "TAX",
    ]

    corporate_patterns = [
        "COMPANY",
        "SEBI",
        "INSOLVENCY",
        "IBC",
        "CORPORATE",
        "DIRECTOR",
    ]

    if any(p in text for p in tax_patterns + corporate_patterns):
        return "Taxation & Corporate"

    # =========================================
    # 🔥 ACT-BASED FALLBACK
    # =========================================
    if acts:
        acts_text = " ".join(acts).upper()

        if any(x in acts_text for x in ["IPC", "CRPC", "NDPS"]):
            return "Criminal"

        if any(x in acts_text for x in ["CPC", "CONTRACT"]):
            return "Civil"

        if any(x in acts_text for x in ["GST", "INCOME TAX"]):
            return "Taxation & Corporate"

    # =========================================
    # 🔥 FINAL FALLBACK (NO MORE "Other")
    # =========================================
    return "Civil"
