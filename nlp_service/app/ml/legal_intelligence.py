import re

# -------------------------------
# 1. CATEGORY DETECTION (STRONG)
# -------------------------------
def classify_category_strict(text: str) -> str:
    t = text.upper()

    if "CRIMINAL APPELLATE JURISDICTION" in t or "CRIMINAL APPEAL" in t:
        return "Criminal"
    if "CIVIL APPELLATE JURISDICTION" in t or "CIVIL APPEAL" in t:
        return "Civil"
    if "SERVICE" in t or "DISCIPLINARY" in t:
        return "Service Law"
    if "TAX" in t or "INCOME TAX" in t or "CIT" in t:
        return "Taxation & Corporate"

    return "Civil"  # safe default

# -------------------------------
# 2. COURT DETECTION (ROBUST)
# -------------------------------
def detect_court_strict(text: str) -> str:
    t = text.upper()

    if "SUPREME COURT OF INDIA" in t:
        return "SUPREME COURT OF INDIA"

    m = re.search(r"HIGH COURT OF ([A-Z ]+)", t)
    if m:
        return f"HIGH COURT OF {m.group(1).strip()}"

    return "SUPREME COURT OF INDIA"  # better default

# -------------------------------
# 3. POINTS OF LAW (NO MORE 'GENERAL ISSUE')
# -------------------------------
POINT_MAP = [
    (r"INTERPRETATION|CONSTRUCTION|STATUTE", "Statutory Interpretation"),
    (r"LEGISLATIVE INTENT", "Legislative Intent"),
    (r"JURISDICTION", "Jurisdiction"),
    (r"APPEAL", "Appellate Jurisdiction"),
    (r"CONTRACT|AGREEMENT", "Contract Law"),
    (r"NEGLIGENCE|LIABILITY", "Tort / Liability"),
    (r"TAX|INCOME TAX|CIT", "Taxation"),
]

def extract_points_smart(text: str):
    t = text.upper()
    points = []

    for pattern, label in POINT_MAP:
        if re.search(pattern, t):
            points.append(label)

    if not points:
        # fallback but meaningful
        points.append("Statutory Interpretation")

    return list(set(points))

# -------------------------------
# 4. ACT DETECTION (BASIC UPGRADE)
# -------------------------------
ACT_MAP = [
    (r"INCOME TAX", "Income Tax Act"),
    (r"IPC|INDIAN PENAL CODE", "Indian Penal Code"),
    (r"CRPC|CRIMINAL PROCEDURE", "CrPC"),
    (r"CPC|CIVIL PROCEDURE", "CPC"),
    (r"CONTRACT", "Indian Contract Act"),
]

def detect_acts_smart(text: str):
    t = text.upper()
    acts = []

    for pattern, label in ACT_MAP:
        if re.search(pattern, t):
            acts.append(label)

    return list(set(acts))
