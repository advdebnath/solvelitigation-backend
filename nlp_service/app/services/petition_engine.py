from datetime import datetime


# =========================================
# 🔥 CLEAN TEXT
# =========================================
def clean(t):
    return str(t).replace("\xa0", " ").strip()


# =========================================
# 🔥 MAIN COURT MODE ENGINE
# =========================================
def generate_petition(structured_docs, query, precedents=None, intelligence=None):
    paragraphs = structured_docs.get("paragraphs", [])
    annexures = structured_docs.get("annexures", [])

    issue = intelligence.get("issue") if intelligence else None
    ratio = intelligence.get("ratio") if intelligence else []
    reasoning = intelligence.get("reasoning") if intelligence else []

    # =========================================
    # 🔥 ISSUE
    # =========================================
    if not issue:
        issue = f"Whether the present case involves {query} and requires judicial intervention?"

    # =========================================
    # 🔥 FACTS
    # =========================================
    facts = ""
    for p in paragraphs[:10]:
        facts += f"Para {p['para_no']}: {clean(p['text'])}\n"

    # =========================================
    # 🔥 STATUTORY ANALYSIS
    # =========================================
    statutory = f"""
The present matter relates to {query}. It is a settled principle that statutes must be interpreted
in a manner that advances the object of the legislation and prevents arbitrariness.

The authorities have failed to apply the correct principles of interpretation, thereby causing
serious prejudice to the petitioner.
"""

    # =========================================
    # 🔥 PRECEDENT ANALYSIS
    # =========================================
    precedent_text = ""
    if precedents:
        for case in precedents[:3]:
            case_no = case.get("caseNumber")
            case_ratio = case.get("ratio")

            if isinstance(case_ratio, list):
                case_ratio = ", ".join(case_ratio)

            precedent_text += f"- {case_no}: {clean(case_ratio)}\n"
    else:
        precedent_text = "- No direct precedent found; reliance on general principles\n"

    # =========================================
    # 🔥 GROUNDS (INTELLIGENT)
    # =========================================
    grounds = f"""
A. Because the impugned action is arbitrary and violative of principles of natural justice.

B. Because the authorities failed to interpret the law correctly in relation to {query}.

C. Because the statutory provisions have been misapplied leading to injustice.

D. Because judicial precedents clearly support the petitioner:
{precedent_text}
"""

    # =========================================
    # 🔥 ADD RATIO SUPPORT
    # =========================================
    if ratio:
        grounds += "\nE. Because the settled legal position is:\n"
        for r in ratio[:3]:
            grounds += f"- {clean(r)}\n"

    # =========================================
    # 🔥 REASONING SUPPORT
    # =========================================
    reasoning_text = ""
    if reasoning:
        reasoning_text = "\n🧠 JUDICIAL REASONING:\n"
        for r in reasoning[:5]:
            reasoning_text += f"- {clean(r)}\n"

    # =========================================
    # 🔥 PRAYER
    # =========================================
    prayer = f"""
It is therefore most respectfully prayed that this Hon’ble Court may be pleased to:

a) Set aside the impugned action/order;
b) Declare the action illegal and void;
c) Grant relief in favour of the petitioner;
d) Pass any other order deemed fit in the interest of justice.
"""

    # =========================================
    # 🔥 ANNEXURES
    # =========================================
    annexure_text = ""
    for a in annexures:
        annexure_text += f"- Annexure {a}\n"

    # =========================================
    # 🔥 FINAL PETITION
    # =========================================
    petition = f"""
IN THE HON'BLE COURT

📌 SUBJECT:
{query}

📌 ISSUE:
{issue}

📜 FACTS OF THE CASE:
{facts}

⚖️ STATUTORY ANALYSIS:
{statutory}

📚 PRECEDENT ANALYSIS:
{precedent_text}

⚖️ GROUNDS:
{grounds}

{reasoning_text}

🙏 PRAYER:
{prayer}

📎 ANNEXURES:
{annexure_text}

Filed on: {datetime.utcnow().date()}
"""

    return petition
