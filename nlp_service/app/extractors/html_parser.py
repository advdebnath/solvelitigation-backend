import re

from bs4 import BeautifulSoup

# =========================================================
# 🔥 CLEAN TEXT
# =========================================================


def clean_text(text):

    if not text:

        return ""

    text = text.replace("\xa0", " ")

    text = text.replace("\n", " ")

    text = text.replace("\r", " ")

    text = text.replace("\t", " ")

    # =====================================================
    # 🔥 FIX OCR HYPHENS
    # =====================================================

    text = re.sub(r"-\s+", "", text)

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 REMOVE NOISE
# =========================================================


def is_noise(text):

    if not text:

        return True

    lower = text.lower().strip()

    noise_patterns = [
        r"^page\s+\d+",
        r"digitally signed",
        r"signature not verified",
        r"downloaded on",
        r"scanned with",
        r"uploaded on",
        r"www\.",
        r"^\d+$",
        r"^\s*$",
        r"^http",
        r"^https",
        r"^cid:",
        r"^img",
        r"^untitled",
    ]

    for pattern in noise_patterns:

        if re.search(pattern, lower):

            return True

    return False


# =========================================================
# 🔥 EXTRACT TABLES
# =========================================================


def extract_tables(soup):

    tables = []

    try:

        for table in soup.find_all("table"):

            rows_data = []

            rows = table.find_all("tr")

            for row in rows:

                cols = row.find_all(["td", "th"])

                row_data = []

                for col in cols:

                    value = clean_text(col.get_text(" ", strip=True))

                    if value:

                        row_data.append(value)

                if row_data:

                    rows_data.append(row_data)

            if rows_data:

                tables.append(rows_data)

    except Exception as e:

        print("❌ TABLE EXTRACTION ERROR:", e)

    return tables


# =========================================================
# 🔥 EXTRACT FOOTNOTES
# =========================================================


def extract_footnotes(soup):

    footnotes = []

    try:

        for tag in soup.find_all(["sup", "footnote"]):

            text = clean_text(tag.get_text(" ", strip=True))

            if text and len(text) < 200:

                footnotes.append(text)

    except Exception as e:

        print("❌ FOOTNOTE EXTRACTION ERROR:", e)

    return list(dict.fromkeys(footnotes))


# =========================================================
# 🔥 EXTRACT CITATIONS
# =========================================================


def extract_citations(text):

    citations = []

    patterns = [
        r"\(\d{4}\)\s*\d+\s*SCC\s*\d+",
        r"AIR\s*\d{4}\s*SC\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*SC\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCR\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCALE\s*\d+",
        r"\(\d{4}\)\s*\d+\s*ALL\s*ER\s*\d+",
    ]

    try:

        for pattern in patterns:

            matches = re.findall(pattern, text, re.I)

            citations.extend(matches)

    except Exception as e:

        print("❌ CITATION EXTRACTION ERROR:", e)

    return list(dict.fromkeys(citations))


# =========================================================
# 🔥 EXTRACT HEADINGS
# =========================================================


def extract_headings(soup):

    headings = []

    try:

        tags = soup.find_all(["h1", "h2", "h3", "b", "strong"])

        for tag in tags:

            text = clean_text(tag.get_text(" ", strip=True))

            if text and len(text) < 300 and text.isupper():

                headings.append(text)

    except Exception as e:

        print("❌ HEADING EXTRACTION ERROR:", e)

    return list(dict.fromkeys(headings))


# =========================================================
# 🔥 EXTRACT PARAGRAPHS
# =========================================================


def extract_paragraphs(soup):

    paragraphs = []

    try:

        # =================================================
        # 🔥 REAL PDFTOHTML STRUCTURE
        # =================================================

        tags = soup.find_all(["div", "p", "span"])

        current_para = ""

        for tag in tags:

            text = clean_text(tag.get_text(" ", strip=True))

            # =============================================
            # 🔥 SKIP NOISE
            # =============================================

            if is_noise(text):

                continue

            if len(text) < 2:

                continue

            # =============================================
            # 🔥 SKIP PAGE NUMBERS
            # =============================================

            if re.fullmatch(r"\d+", text):

                continue

            # =============================================
            # 🔥 SKIP TABLE CONTENT
            # =============================================

            if tag.find_parent("table"):

                continue

            # =============================================
            # 🔥 SMART PARAGRAPH DETECTION
            # =============================================

            starts_new = False

            # =============================================
            # 🔥 NUMBERED PARAGRAPHS
            # =============================================

            if re.match(r"^\d+\.", text):

                starts_new = True

            # =============================================
            # 🔥 VERY LARGE PARAGRAPH SPLIT
            # =============================================

            elif len(current_para) > 1800:

                starts_new = True

            # =============================================
            # 🔥 HEADING DETECTION
            # =============================================

            elif len(text) < 120 and text.isupper() and len(text.split()) < 12:

                starts_new = True

            # =============================================
            # 🔥 COURT TITLE
            # =============================================

            elif "SUPREME COURT" in text or "HIGH COURT" in text:

                starts_new = True

            # =============================================
            # 🔥 START NEW
            # =============================================

            if starts_new:

                if len(current_para.split()) > 8:

                    paragraphs.append(current_para.strip())

                current_para = text

            else:

                # =========================================
                # 🔥 FIX OCR HYPHEN SPLITS
                # =========================================

                if current_para.endswith("-"):

                    current_para = current_para[:-1] + text

                else:

                    current_para += " " + text

        # =============================================
        # 🔥 LAST PARAGRAPH
        # =============================================

        if len(current_para.split()) > 8:

            paragraphs.append(current_para.strip())

        # =============================================
        # 🔥 DEDUPLICATE
        # =============================================

        cleaned = []

        seen = set()

        for para in paragraphs:

            short = re.sub(r"\s+", " ", para[:300].lower())

            if short not in seen:

                seen.add(short)

                cleaned.append(para)

        return cleaned

    except Exception as e:

        print("❌ PARAGRAPH EXTRACTION ERROR:", e)

        return []


# =========================================================
# 🔥 MAIN PARSER
# =========================================================


def parse_html_document(html):

    try:

        if not html:

            return {
                "paragraphs": [],
                "headings": [],
                "footnotes": [],
                "tables": [],
                "citations": [],
                "clean_text": "",
                "raw_html": "",
                "confidence": 0,
            }

        soup = BeautifulSoup(html, "html.parser")

        # =================================================
        # 🔥 REMOVE SCRIPT/STYLE
        # =================================================

        for bad in soup(["script", "style", "meta", "link"]):

            bad.decompose()

        # =================================================
        # 🔥 EXTRACT
        # =================================================

        paragraphs = extract_paragraphs(soup)

        headings = extract_headings(soup)

        footnotes = extract_footnotes(soup)

        tables = extract_tables(soup)

        clean_joined = " ".join(paragraphs)

        citations = extract_citations(clean_joined)

        # =================================================
        # 🔥 CONFIDENCE
        # =================================================

        confidence = 50

        if len(paragraphs) > 10:

            confidence += 20

        if headings:

            confidence += 10

        if citations:

            confidence += 10

        if footnotes:

            confidence += 5

        if tables:

            confidence += 5

        confidence = min(confidence, 95)

        result = {
            "paragraphs": paragraphs,
            "headings": headings,
            "footnotes": footnotes,
            "tables": tables,
            "citations": citations,
            "clean_text": clean_joined,
            "raw_html": html,
            "confidence": confidence,
        }

        print(
            "✅ HTML Parsed:",
            {
                "paragraphs": len(paragraphs),
                "headings": len(headings),
                "footnotes": len(footnotes),
                "tables": len(tables),
                "citations": len(citations),
                "confidence": confidence,
            },
        )

        return result

    except Exception as e:

        print("❌ HTML PARSER ERROR:", e)

        return {
            "paragraphs": [],
            "headings": [],
            "footnotes": [],
            "tables": [],
            "citations": [],
            "clean_text": "",
            "raw_html": html,
            "confidence": 0,
        }
