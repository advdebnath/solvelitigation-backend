# Case Number Regression Suite

This suite validates judiciary caption extraction across:

- Supreme Court
- High Courts
- Tribunals
- OCR-corrupted judgments
- malformed headers
- legacy JUDIS scans

## Structure

fixtures/
    raw input text fixtures

expected/
    canonical expected extraction outputs

outputs/
    generated runtime outputs

## Goals

- prevent extraction regressions
- stabilize OCR handling
- validate caption preservation
- validate semantic normalization
- ensure canonical numbering consistency

## Execution

python3 tests/case_number/run_case_number_tests.py
