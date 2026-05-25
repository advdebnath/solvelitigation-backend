import json
import sys

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

sys.path.insert(0, str(ROOT))

from app.extractors.case_number_extractor import extract_case_number


BASE = Path(__file__).parent

fixture_root = BASE / "fixtures"
expected_root = BASE / "expected"

fixture_files = list(
    fixture_root.rglob("*.txt")
)

total = 0
passed = 0

for fixture in fixture_files:

    relative = fixture.relative_to(fixture_root)

    expected_file = (
        expected_root /
        relative.parent /
        (fixture.stem + ".json")
    )

    if not expected_file.exists():

        print(f"❌ Missing expected file: {expected_file}")
        continue

    text = fixture.read_text()

    result = extract_case_number(text)

    expected = json.loads(
        expected_file.read_text()
    )

    print("=" * 80)
    print("FIXTURE:", relative)
    print("=" * 80)

    ok = True

    for key, expected_value in expected.items():

        actual_value = result.get(key)

        if actual_value != expected_value:

            ok = False

            print(f"❌ {key}")
            print("EXPECTED:", expected_value)
            print("ACTUAL  :", actual_value)

        else:

            print(f"✅ {key}: {actual_value}")

    total += 1

    if ok:
        passed += 1

    print()

print("=" * 80)
print(f"PASSED: {passed}/{total}")
print("=" * 80)
