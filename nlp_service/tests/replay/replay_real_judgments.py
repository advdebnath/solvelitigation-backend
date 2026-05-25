import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))

import fitz

from app.extractors.case_number_extractor import (
    extract_case_number
)

from app.extractors.judge_extractor import (
    extract_judges
)


PDF_ROOT = Path(
    "/var/www/solvelitigation/backend/uploads/judgments"
)

pdfs = list(
    PDF_ROOT.glob("*.pdf")
)[:25]


print("=" * 120)
print("🔥 REAL JUDICIARY REPLAY VALIDATION")
print("=" * 120)


for pdf_path in pdfs:

    try:

        print("\n")
        print("=" * 120)
        print(f"📄 FILE: {pdf_path.name}")
        print("=" * 120)

        doc = fitz.open(pdf_path)

        full_text = ""

        for page in doc:

            try:
                full_text += page.get_text()

            except Exception:
                pass

        doc.close()

        case_data = extract_case_number(
            full_text
        )

        judges = extract_judges(
            full_text
        )

        print("✅ CASE NUMBER:")
        print(
            case_data.get(
                "case_number"
            )
        )

        print("\n✅ COURT TYPE:")
        print(
            case_data.get(
                "court_type"
            )
        )

        print("\n✅ SOURCE:")
        print(
            case_data.get(
                "source"
            )
        )

        print("\n✅ CONFIDENCE:")
        print(
            case_data.get(
                "confidence"
            )
        )

        print("\n✅ JUDGES:")
        print(judges)

    except Exception as e:

        print("❌ REPLAY FAILURE:")
        print(str(e))
