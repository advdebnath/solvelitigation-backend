import re
from datetime import datetime

from dateutil import parser

# =========================================================
# 🔥 MONTH MAP
# =========================================================

MONTHS = {
    "JANUARY": "01",
    "FEBRUARY": "02",
    "MARCH": "03",
    "APRIL": "04",
    "MAY": "05",
    "JUNE": "06",
    "JULY": "07",
    "AUGUST": "08",
    "SEPTEMBER": "09",
    "OCTOBER": "10",
    "NOVEMBER": "11",
    "DECEMBER": "12",
}


MONTHS.update({
    "JAN":"01",
    "FEB":"02",
    "MAR":"03",
    "APR":"04",
    "JUN":"06",
    "JUL":"07",
    "AUG":"08",
    "SEP":"09",
    "SEPT":"09",
    "OCT":"10",
    "NOV":"11",
    "DEC":"12",
})

# =========================================================
# 🔥 FORMAT DATE
# =========================================================


def format_date(day, month, year):

    try:

        month_num = MONTHS.get(month.upper())

        if not month_num:

            return None

        dt = datetime.strptime(f"{year}-{month_num}-{int(day):02d}", "%Y-%m-%d")

        return dt.strftime("%Y-%m-%d")

    except Exception:

        return None


# =========================================================
# 🔥 YEAR VALIDATION
# =========================================================


def is_valid_year(year):

    try:

        year = int(year)

        return 1950 <= year <= 2050

    except Exception:

        return False


# =========================================================
# 🔥 UNIVERSAL DATE NORMALIZER
# =========================================================


def normalize_any_date(raw):

    try:

        if not raw:
            return None

        raw = str(raw)

        # =================================================
        # 🔥 OCR FIXES
        # =================================================

        raw = raw.replace("O", "0")

        raw = raw.replace("I", "1")

        raw = raw.replace("l", "1")

        raw = re.sub(r"\s+", " ", raw).strip()

        # =================================================
        # 🔥 REMOVE LABELS
        # =================================================

        raw = re.sub(
            r"^(DATED|DATE|PRONOUNCED ON|DELIVERED ON|NEW DELHI)\s*[:\-;,]*\s*",
            "",
            raw,
            flags=re.I,
        )

        # =================================================
        # 🔥 SMART PARSE
        # =================================================

        dt = parser.parse(raw, fuzzy=True, dayfirst=True)

        # =================================================
        # 🔥 YEAR VALIDATION
        # =================================================

        if dt.year < 1950 or dt.year > 2050:
            return None

        return dt.strftime("%Y-%m-%d")

    except Exception:

        return None


# =========================================================
# 🔒 AUTHORITATIVE JUDGMENT YEAR LOCK
# =========================================================


def build_authoritative_year(date_value):

    try:

        if not date_value:
            return None

        dt = parser.parse(str(date_value), fuzzy=True, dayfirst=True)

        year = dt.year

        if year < 1950 or year > 2050:
            return None

        return str(year)

    except Exception:

        return None


# =========================================================
# 🔥 EXTRACT JUDGMENT DATE
# =========================================================


def extract_judgment_date(text):

    try:

        if not text:

            return {"date": None, "confidence": 0}

        if not isinstance(text, str):
            text = str(text)

        # =================================================
        # 🔥 FOOTER PRIORITY
        # =================================================

        footer_zone = text[-10000:]

        # =============================================
        # 🔥 FOOTER DATE CANDIDATE NORMALIZATION
        # =============================================

        footer_zone = re.sub(
            r"(NEW\s+DELHI\s+\d{1,2}(?:ST|ND|RD|TH)?\s+[A-Z]+\s*,?\s+\d{4})",
            r"\n\1\n",
            footer_zone,
            flags=re.I
        )

        footer_zone = re.sub(
            r"(DATE\s*:\s*\d{4}[.\-/]\d{1,2}[.\-/]\d{1,2})",
            r"\n\1\n",
            footer_zone,
            flags=re.I
        )

        print("📅 FOOTER DATE SCAN ACTIVE")
        print("🔥 DATE EXTRACTOR VERSION: JUN03_AUDIT_V1")

        # =================================================
        # 🔥 FOOTER LINES
        # =================================================

        footer_lines = footer_zone.splitlines()

        footer_lines = [
            x.strip()
            for x in footer_lines
            if x.strip()
        ]

        print(f"📅 FOOTER LINE COUNT: {len(footer_lines)}")

        for x in footer_lines[-20:]:
            print(f"📅 FOOTER RAW: {repr(x)}")


        # =================================================
        # 🔥 REVERSE FOOTER SCAN
        # =================================================

        for idx, line in reversed(list(enumerate(footer_lines))):

            clean = line.strip()

            upper = clean.upper()

            print(f"📅 SCANNING LINE: {repr(upper)}")


            # =============================================
            # 🔥 REMOVE DATE LABELS
            # =============================================

            upper = re.sub(
                r"^(DATED|DATE|PRONOUNCED ON|DELIVERED ON)\s*[:\-]*\s*",
                "",
                upper,
                flags=re.I,
            )

            if not upper:

                continue

            # =============================================
            # 🔥 IGNORE LARGE OCR BLOCKS
            # =============================================

            if len(upper) > 80:

                continue

            # =============================================
            # 🔥 MUST CONTAIN MONTH
            # =============================================

            has_month = any(month in upper for month in MONTHS)

            has_numeric_date = bool(
                re.search(
                    r"\b\d{1,4}[./-]\d{1,2}[./-]\d{1,4}\b",
                    upper
                )
            )

            if not has_month and not has_numeric_date:

                continue

            print("📅 Footer Candidate:", upper)
            print("📅 Footer Candidate Length:", len(upper))

            # =============================================
            # 🔥 PURE FOOTER DATE PRIORITY
            # =============================================

            court_style = re.search(
                r"(?:NEW\s+DELHI\s+)?"
                r"(\d{1,2})(?:ST|ND|RD|TH)?"
                r"(?:\s+DAY\s+OF)?"
                r"[\s,]+"
                r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)"
                r"[\s,]+"
                r"(\d{4})",
                upper,
                re.I
            )

            if court_style:

                result = {
                    "date": format_date(
                        court_style.group(1),
                        court_style.group(2),
                        court_style.group(3)
                    ),
                    "confidence": 99
                }

                print("✅ COURT STYLE DATE:", result)

                return result

            pure_match = re.search(
                r"^(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[\s\.,;:-]+(\d{1,2})[\s\.,;:-]+(\d{4})",
                upper,
                re.I,
            )

            if pure_match:

                month = pure_match.group(1)
                day = pure_match.group(2)
                year = pure_match.group(3)

            else:

                # =============================================
                # 🔥 DAY FIRST FORMAT
                # =============================================

                reverse_match = re.search(
                    r"^(\d{1,2})(?:ST|ND|RD|TH)?[\s\.,;:-]+(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER)[\s\.,;:-]+(\d{4})",
                    upper,
                    re.I,
                )

                if not reverse_match:
                    continue

                day = reverse_match.group(1)
                month = reverse_match.group(2)
                year = reverse_match.group(3)

                month = re.sub(r"[^A-Z]", "", month.upper())

                day = re.sub(r"\D", "", day)

                year = re.sub(r"\D", "", year)

                print(
                    "📅 Parsed Footer Date:", {"day": day, "month": month, "year": year}
                )

                if is_valid_year(year):

                    formatted = format_date(day, month, year)

                    if formatted:

                        result = {"date": formatted, "confidence": 99}

                        print("✅ Footer Judgment Date:", result)

                        return result

            # =============================================
            # 🔥 OCR-TOLERANT FALLBACK
            # =============================================

            match = re.search(
                r"(JANUARY|FEBRUARY|MARCH|APRIL|MAY|JUNE|JULY|AUGUST|SEPTEMBER|OCTOBER|NOVEMBER|DECEMBER).*?(\d{1,2}).*?(\d{4})",
                upper,
                re.I,
            )

            if not match:

                continue

            month = match.group(1)
            day = match.group(2)
            year = match.group(3)

            month = re.sub(r"[^A-Z]", "", month.upper())

            day = re.sub(r"\D", "", day)

            year = re.sub(r"\D", "", year)

            print(
                "📅 Parsed OCR Footer Date:", {"day": day, "month": month, "year": year}
            )

            if not is_valid_year(year):

                continue

            formatted = format_date(day, month, year)

            if not formatted:

                continue

            result = {"date": formatted, "confidence": 95}

            print("✅ OCR Footer Judgment Date:", result)

            return result


        # =================================================
        # 🔥 YEAR-FIRST NUMERIC
        # =================================================

        year_first = re.findall(
            r"(19\d{2}|20\d{2})[.\-/](\d{1,2})[.\-/](\d{1,2})",
            text
        )

        for item in year_first:

            year, month, day = item

            try:

                dt = datetime.strptime(
                    f"{year}-{month}-{day}",
                    "%Y-%m-%d"
                )

                result = {
                    "date": dt.strftime("%Y-%m-%d"),
                    "confidence": 90
                }

                print("✅ Year First Judgment Date:", result)

                return result

            except Exception:

                continue

        # =================================================
        # 🔥 FALLBACK NUMERIC
        # =================================================

        numeric = re.findall(r"(\d{1,2})[.\-/](\d{1,2})[.\-/](\d{4})", text)

        for item in numeric:

            day, month, year = item

            try:

                dt = datetime.strptime(f"{year}-{month}-{day}", "%Y-%m-%d")

                result = {"date": dt.strftime("%Y-%m-%d"), "confidence": 60}

                print("✅ Numeric Judgment Date:", result)

                return result

            except Exception:

                continue

        # =================================================
        # 🔥 UNIVERSAL FALLBACK PARSER
        # =================================================

        universal = normalize_any_date(text)

        if universal:

            result = {"date": universal, "confidence": 85}

            print("✅ Universal Date Parser:", result)

            return result

        return {"date": None, "confidence": 0}

    except Exception as e:

        print("❌ DATE EXTRACTION ERROR:", e)

        return {"date": None, "confidence": 0}


# =========================================================
# 🔥 DIRECT TEST
# =========================================================

if __name__ == "__main__":

    sample = """
    NEW DELHI;
    APRIL 05, 2021.
    """

    print(extract_judgment_date(sample))
