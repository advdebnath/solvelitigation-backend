import re


RATIO_HINTS = [

    "held",
    "we hold",
    "we are of the opinion",
    "we are of the view",
    "it is held",
    "therefore",
    "thus",
    "in our opinion",
    "the court held",
    "the appeal is allowed",
    "the appeal is dismissed",
    "petition allowed",
    "petition dismissed"
]

ADVANCED_RATIO_HINTS = [

    "we do not find any merit",
    "the high court erred",
    "it cannot be said",
    "it is evident",
    "it is clear",
    "we find that",
    "we conclude",
    "the respondents are not entitled",
    "the appellants are entitled",
    "within the meaning of article",
    "principles of natural justice",
    "equal pay for equal work",
    "article 14",
    "article 16",
    "state within the meaning of article 12",
    "the writ petition is dismissed",
    "the writ petition is allowed",
    "the appeals are directed against",
    "the question is",
    "the issue is",
    "the court finds"
]



def extract_ratio(
    text,
    jurisprudential_chunks=None
):

    if jurisprudential_chunks is None:
        jurisprudential_chunks = []


    # =====================================================
    # 🔥 JURISPRUDENTIAL SENTENCE SEGMENTATION
    # =====================================================

    paragraphs = re.split(
        r'(?<=[\\.!\\?])\\s+(?='
        r'(?:It|Thus|Therefore|Hence|Accordingly|'
        r'We|The Court|In the result|'
        r'The petitions|The appeals|'
        r'Under Article|When an authority|'
        r'If the Government|'
        r'It becomes apparent|'
        r'The Government)'
        r')',
        text
    )

    if len(paragraphs) <= 3:

        paragraphs = re.split(
            r'(?<=[\\.!\\?])\\s+',
            text
        )

    ratio_candidates = []

    for para in paragraphs:

        clean_para = para.strip()

        if len(clean_para) < 50:
            continue

        lower_para = clean_para.lower()

        # =====================================================
        # 🔥 HARD OCR / HEADER POLLUTION REJECTION
        # =====================================================

        hard_pollution_hits = [

            "http://judis.nic.in",
            "page 1 of",
            "page 2 of",
            "petitioner:",
            "respondent:",
            "date of judgment:",
            "bench:",
            "supreme court of india"
        ]

        pollution_score = sum(
            1
            for patt in hard_pollution_hits
            if patt in lower_para
        )

        if pollution_score >= 3:
            continue

        if lower_para.count("supreme court of india") >= 2:
            continue

        if lower_para.count("http://judis") >= 1:
            continue

        score = 0

        for hint in RATIO_HINTS:

            if hint in lower_para:
                score += 20

        for adv_hint in ADVANCED_RATIO_HINTS:

            if adv_hint in lower_para:
                score += 35


        if "section" in lower_para:
            score += 5

        if "act" in lower_para:
            score += 5

        
        polluted_patterns = [

          "http://judis",
          "supreme court of india",
          "page 1 of",
          "page 2 of",
          "petitioner:",
          "respondent:",
          "date of judgment",
          "bench:"
        ]

        is_polluted = any(
          patt in lower_para
          for patt in polluted_patterns
        )

        if (
          is_polluted
          or clean_para.count("\n") > 10
          or len(clean_para.split()) > 220
          or len(clean_para) > 4000
        ):
          continue

        if score >= 20:

          ratio_candidates.append({
              "text": clean_para,
              "score": score
          })


    # =====================================================
    # 🔥 JURISPRUDENTIAL CHUNK ANALYSIS
    # =====================================================

    for chunk in jurisprudential_chunks:

        chunk_text = str(
            chunk.get("text", "")
        ).strip()

        if len(chunk_text) < 80:
            continue

        chunk_type = str(
            chunk.get("chunk_type", "")
        ).upper()

        importance = int(
            chunk.get("importance", 0)
        )

        lower_chunk = chunk_text.lower()

        # =====================================================
        # 🔥 HARD OCR / HEADER POLLUTION REJECTION
        # =====================================================

        hard_pollution_hits = [

            "http://judis.nic.in",
            "page 1 of",
            "page 2 of",
            "petitioner:",
            "respondent:",
            "date of judgment:",
            "bench:",
            "supreme court of india"
        ]

        pollution_score = sum(
            1
            for patt in hard_pollution_hits
            if patt in lower_chunk
        )

        if pollution_score >= 3:
            continue

        if lower_chunk.count("supreme court of india") >= 2:
            continue

        if lower_chunk.count("http://judis") >= 1:
            continue

        score = 0

        for hint in RATIO_HINTS:

            if hint in lower_chunk:
                score += 25

        for adv_hint in ADVANCED_RATIO_HINTS:

            if adv_hint in lower_chunk:
                score += 40


        if "section" in lower_chunk:
            score += 10

        if "act" in lower_chunk:
            score += 10

        if "held" in lower_chunk:
            score += 20

        if "ratio decidendi" in lower_chunk:
            score += 40

        if chunk_type == "RATIO_DECIDENDI":
            score += 120

        if chunk_type == "OPERATIVE_ORDER":
            score += 80

        score += min(
            importance,
            200
        )

        
        polluted_patterns = [

          "http://judis",
          "supreme court of india",
          "page 1 of",
          "page 2 of",
          "petitioner:",
          "respondent:",
          "date of judgment",
          "bench:"
        ]

        is_polluted = any(
          patt in lower_chunk
          for patt in polluted_patterns
        )

        if (
          is_polluted
          or chunk_text.count("\n") > 12
          or len(chunk_text.split()) > 260
          or len(chunk_text) > 5000
        ):
          continue

        if score >= 60:

          ratio_candidates.append({
              "text": chunk_text,
              "score": score,
              "source": "jurisprudential_chunk",
              "chunk_type": chunk_type
          })

    ratio_candidates = sorted(
        ratio_candidates,
        key=lambda x: x["score"],
        reverse=True
    )

    best_ratio = (
        ratio_candidates[0]["text"]
        if ratio_candidates
        else ""
    )

    return {
        "ratio": best_ratio,
        "confidence":
            min(
                95,
                40 + len(ratio_candidates) * 5
            ),
        "candidates":
            ratio_candidates[:5]
    }