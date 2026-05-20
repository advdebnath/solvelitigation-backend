import re
from typing import List, Dict


# =========================================================
# 🔥 LEGAL SAFE ABBREVIATIONS
# =========================================================

PROTECTED_ABBREVIATIONS = [

    "Cr.P.C.",
    "I.P.C.",
    "C.P.C.",
    "Art.",
    "Arts.",
    "Const.",
    "Anr.",
    "Ors.",
    "Govt.",
    "Dept.",
    "Co.",
    "Corp.",
    "Pvt.",
    "Hon'ble.",
    "Addl.",
    "Misc.",
    "Reg.",
    "Rs.",
    "M.P.",
    "A.P.",
    "UOI.",


    "v.",
    "vs.",
    "Mr.",
    "Mrs.",
    "Dr.",
    "Jr.",
    "Sr.",
    "No.",
    "Nos.",
    "Sec.",
    "SCC.",
    "AIR.",
    "Cri.",
    "Ltd.",
    "JJ.",
    "J.",
    "W.P.",
    "S.L.P.",
    "u/s.",
]


# =========================================================
# 🔥 NORMALIZE TEXT
# =========================================================

def normalize_text(text: str) -> str:

    if not text:
        return ""

    # -------------------------------------------------
    # REMOVE OCR / DIGITAL SIGNATURE NOISE
    # -------------------------------------------------

    text = re.sub(r"Digitally signed by[^\n]*", " ", text, flags=re.I)
    text = re.sub(r"Uploaded on -[^\n]*", " ", text, flags=re.I)
    text = re.sub(r"Downloaded on -[^\n]*", " ", text, flags=re.I)
    text = re.sub(r"Page\s+\d+\s+of\s+\d+", " ", text, flags=re.I)

    # -------------------------------------------------
    # REMOVE OCR TIMESTAMPS / COURT EXPORT NOISE
    # -------------------------------------------------

    text = re.sub(r"\b\d{1,2}:\d{2}:\d{2}\s*IST\b", " ", text, flags=re.I)

    text = re.sub(r"\bReason:\b", " ", text, flags=re.I)

    text = re.sub(r"\bDownloaded\s+on\s*:\s*[^\n]*", " ", text, flags=re.I)

    # -------------------------------------------------
    # REMOVE INLINE FOOTNOTE ARTIFACTS
    # -------------------------------------------------

    text = re.sub(
        r"\bHereinafter\s+referred\s+to\s+as\b[^\.;]{0,120}",
        " ",
        text,
        flags=re.I
    )

    text = re.sub(
        r"\b\d+\s+Hereinafter\b",
        " ",
        text,
        flags=re.I
    )

    # -------------------------------------------------
    # REMOVE SCANNING / DIGITAL EXPORT ARTIFACTS
    # -------------------------------------------------

    text = re.sub(r"\bSigned\s+by\b[^\n]*", " ", text, flags=re.I)

    text = re.sub(r"\bDigitally\s+signed\b[^\n]*", " ", text, flags=re.I)


    # -------------------------------------------------
    # REMOVE EXCESS DOTS / OCR GARBAGE
    # -------------------------------------------------

    text = re.sub(r"\.{3,}", " ", text)
    text = re.sub(r"[_•▪■]+", " ", text)

    # -------------------------------------------------
    # NORMALIZE WHITESPACE
    # -------------------------------------------------

    text = re.sub(r"[ \t]+", " ", text)

    return text.strip()



# =========================================================
# 🔥 PROTECT LEGAL ABBREVIATIONS
# =========================================================

def protect_abbreviations(text: str) -> str:

    protected = text

    for abbr in PROTECTED_ABBREVIATIONS:

        escaped_abbr = re.escape(abbr)

        safe = abbr.replace(".", "__DOT__")

        protected = re.sub(
            escaped_abbr,
            safe,
            protected,
            flags=re.I
        )

    return protected



# =========================================================
# 🔥 RESTORE ABBREVIATIONS
# =========================================================

def restore_abbreviations(text: str) -> str:

    if not isinstance(text, str):
        return ""

    return text.replace("__DOT__", ".")



# =========================================================
# 🔥 MASK LEGAL CITATIONS
# =========================================================

def mask_legal_citations(text: str) -> str:

    if not text:
        return ""

    citation_patterns = [

        r"\(\d{4}\)\s*\d+\s*SCC\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCC\s*\(Cri\)\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCC\s*\(Civ\)\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCC\s*\(L&S\)\s*\d+",
        r"AIR\s*\d{4}\s*SC\s*\d+",
        r"AIR\s*\d{4}\s*[A-Z][A-Za-z]+\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*SC\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*Del\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*Bom\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*[A-Z][A-Za-z]+\s*\d+",
        r"\d{4}\s*Cri\s*LJ\s*\d+",
        r"\(\d{4}\)\s*\d+\s*SCR\s*\d+",
        r"\d{4}\s*ALL\s*MR\s*\d+",
        r"\d{4}\s*Mh\\.L\\.J\\.\s*\d+",
        r"\d{4}\s*KLT\s*\d+",
        r"\d{4}\s*GLR\s*\d+",
        r"\d{4}\s*Gau\s*LR\s*\d+",
        r"\d{4}\s*CTC\s*\d+",
        r"\d{4}\s*LW\s*\d+",
        r"\d{4}\s*JT\s*\d+",
        r"\d{4}\s*SCALE\s*\d+",
    ]

    protected = text

    for idx, pattern in enumerate(citation_patterns):

        matches = re.findall(
            pattern,
            protected
        )

        for m_idx, match in enumerate(matches):

            token = f"__CITATION_{idx}_{m_idx}__"

            protected = protected.replace(
                match,
                token
            )

    return protected

# =========================================================
# 🔥 RESTORE LEGAL CITATIONS
# =========================================================

def restore_legal_citations(original: str, masked: str) -> str:

    if not isinstance(original, str):
        original = ""

    if not isinstance(masked, str):
        masked = ""


    citation_patterns = [

        r"\(\d{4}\)\s*\d+\s*SCC\s*\d+",
        r"AIR\s*\d{4}\s*SC\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*SC\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*Del\s*\d+",
        r"\d{4}\s*SCC\s*OnLine\s*Bom\s*\d+",
        r"\d{4}\s*Cri\s*LJ\s*\d+",
    ]

    restored = masked

    token_index = 0

    for idx, pattern in enumerate(citation_patterns):

        matches = re.findall(pattern, original)

        for m_idx, match in enumerate(matches):

            token = f"__CITATION_{idx}_{m_idx}__"

            restored = restored.replace(token, match)

    return restored


# =========================================================
# 🔥 MASK NUMERIC DOT STRUCTURES
# =========================================================

def mask_numeric_dots(text: str) -> str:

    protected = re.sub(
        r"(\d)\.(\d)",
        r"\1__NUMDOT__\2",
        text
    )

    return protected


def restore_numeric_dots(text: str) -> str:

    if not isinstance(text, str):
        return ""

    return text.replace("__NUMDOT__", ".")






# =========================================================
# 🔥 SENTENCE SPLITTER
# =========================================================

def split_into_sentences(text: str) -> List[str]:

    if not text:
        return []

    text = normalize_text(text)

    protected_text = protect_abbreviations(text)

    protected_text = mask_legal_citations(
        protected_text
    )

    protected_text = mask_numeric_dots(
        protected_text
    )

    paragraphs = re.split(
        r'\n\s*\n+',
        protected_text
    )

    raw_sentences = []

    for para in paragraphs:

        para = para.strip()

        if not para:
            continue

        para_sentences = re.split(
            r'(?<=[.!?])\s+(?=(?:[A-Z0-9]|\(?[ivxlcdm]+\)|\d+\.|[a-z]))',
            para
        )


        raw_sentences.extend(
            para_sentences
        )

    sentences = []

    for sent in raw_sentences:

        sent = restore_abbreviations(sent)

        sent = restore_legal_citations(
            text,
            sent
        )

        sent = restore_numeric_dots(
            sent
        )





        if not isinstance(sent, str):
            continue

        sent = sent.strip()

        if len(sent) < 15:
            continue

        sentences.append(sent)

    return sentences


# =========================================================
# 🔥 MAIN EXTRACTION ENGINE
# =========================================================

def extract_jurisprudential_sentences(
    text: str
) -> List[Dict]:

    if not text:
        return []

    sentences = split_into_sentences(text)

    total = len(sentences)

    results = []

    for idx, sentence in enumerate(sentences):

        results.append({

            "sentence_id": f"S{idx+1}",

            "text": sentence,

            "normalized_text": sentence.lower(),

            "sentence_index": idx,

            "position": round(
                idx / max(total, 1),
                4
            ),

            "word_count": len(sentence.split()),

            "char_count": len(sentence),
        })

    return results

