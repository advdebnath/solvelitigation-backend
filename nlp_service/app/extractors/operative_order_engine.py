import re
from collections import defaultdict
from app.extractors.procedural_history_detector import (
    detect_procedural_history
)

# ============================================================
# 🔥 LEGAL OPERATIVE VERB ONTOLOGY
# ============================================================

LEGAL_OPERATIVE_VERBS = [


    "allowed",
    "dismissed",
    "disposed",
    "quashed",
    "set aside",
    "affirmed",
    "upheld",
    "modified",
    "acquitted",
    "convicted",
    "remanded",
    "reinstated",
    "vacated",
    "reversed",
    "partly allowed",
    "partially allowed",
]


# ============================================================
# 🔥 HISTORICAL / NON-FINAL CONTEXT SUPPRESSION
# ============================================================

HISTORICAL_CONTEXT_MARKERS = [

    "trial court",
    "sessions court",
    "lower court",
    "single judge",
    "division bench",
    "earlier",
    "previously",
    "prior proceedings",
    "before the high court",
    "before the tribunal",
    "impugned judgment",
    "impugned order",
    "learned trial judge",
    "the high court held",
    "the tribunal held",
    "the trial court held",
]


# ============================================================
# 🔥 CATEGORY AWARE DISPOSITION PATTERNS
# ============================================================

DISPOSITION_PATTERNS = {

    "Appeal Allowed": [

        r"\bappeal\s+is\s+allowed\b",
        r"\bappeal\s+stands\s+allowed\b",
        r"\bappeal\s+allowed\b",
        r"\bimpugned\s+judgment\s+set\s+aside\b",
        r"\border\s+set\s+aside\b",

        r"\\bwe\\s+accordingly\\s+allow\\s+the\\s+appeal\\b",

        r"\\ballowed\\s+and\\s+set\\s+aside\\b",

        r"\\bimpugned\\s+judgment\\s+is\\s+set\\s+aside\\b",

        r"\\bjudgment\\s+is\\s+set\\s+aside\\b",

        r"\\bconviction\\s+set\\s+aside\\b",

        r"\\border\\s+quashed\\b",

        r"\\bproceedings\\s+quashed\\b",

        r"\bwrit\s+petition\s+allowed\b",

        r"\bwrit\s+petitions\s+are\s+allowed\b",

        r"\bliable\s+to\s+be\s+quashed\b",

        r"\bset\s+aside\s+all\s+the\s+orders\b",

        r"\borders?\s+.*?\s+quashed\b",

        r"\bthe\s+writ\s+petitions\s+are\s+allowed\b",
    ],

    "Appeal Dismissed": [

        r"\bappeal\s+is\s+dismissed\b",

        r"\bappeal\s+stands\s+dismissed\b",

        r"\bappeal\s+dismissed\b",

        r"\bdismissed\b",

        r"\bthe\s+appeal\s+fails\b",

        r"\bappeal\s+fails\b",

        r"\border\s+upheld\b",

        r"\bjudgment\s+upheld\b",

        r"\bconviction\s+upheld\b",

        r"\bwe\s+find\s+no\s+reason\s+to\s+interfere\b",

        r"\bno\s+reason\s+to\s+interfere\b",

        r"\bno\s+merit\b",

        r"\bdevoid\s+of\s+merit\b",

        r"\bfind\s+no\s+infirmity\b",

        r"\bno\s+infirmity\b",

        r"\binterference\s+is\s+not\s+warranted\b",

        r"\bno\s+case\s+for\s+interference\b",

        r"\bappeal\s+lacks\s+merit\b",

        r"\bwe\s+see\s+no\s+reason\s+to\s+interfere\b",

        r"\bjudgment\s+calls\s+for\s+no\s+interference\b",

        r"\bappeal\s+fails\s+and\s+is\s+dismissed\b",

        r"\bfindings\s+of\s+the\s+courts\s+below\b",

        # ====================================================
        # 🔥 ADVANCED SUPREME COURT DISMISSAL SEMANTICS
        # ====================================================

        r"\bdoes\s+not\s+warrant\s+interference\b",

        r"\bfindings\s+do\s+not\s+call\s+for\s+interference\b",

        r"\bwe\s+find\s+no\s+merit\s+in\s+the\s+appeal\b",

        r"\bappeal\s+is\s+without\s+merit\b",

        r"\bthe\s+appeal\s+deserves\s+to\s+be\s+dismissed\b",

        r"\bwe\s+do\s+not\s+find\s+any\s+ground\s+to\s+interfere\b",

        r"\bno\s+interference\s+is\s+called\s+for\b",

        r"\bjudgment\s+does\s+not\s+suffer\s+from\s+any\s+infirmity\b",
    ],

    "Conviction Upheld": [

        r"\bconviction\s+is\s+upheld\b",
        r"\bconviction\s+affirmed\b",
        r"\bconviction\s+sustained\b",
    ],

    "Acquittal": [

        r"\bacquitted\b",
        r"\bbenefit\s+of\s+doubt\b",
        r"\baccused\s+is\s+acquitted\b",
    ],

    "Remand": [

        r"\bmatter\s+is\s+remanded\b",
        r"\bmatter\s+stands\s+remanded\b",
        r"\bremitted\s+back\b",
        r"\bcase\s+remanded\b",
    ],

    "Sentence Modified": [

        r"\bsentence\s+modified\b",
        r"\bsentence\s+reduced\b",
        r"\bpunishment\s+modified\b",
    ],

    "Termination Quashed": [

        r"\btermination\s+quashed\b",
        r"\bdismissal\s+quashed\b",
        r"\breinstated\s+in\s+service\b",
    ],
}

# ============================================================
# 🔥 DISPOSITION PRIORITY WEIGHTS
# ============================================================

DISPOSITION_WEIGHTS = {

    "Appeal Allowed": 120,

    "Acquittal": 120,

    "Termination Quashed": 115,

    "Remand": 95,

    "Sentence Modified": 90,

    "Appeal Dismissed": 80,

    "Conviction Upheld": 75,

    "Disposed": 30,
}


# ============================================================
# 🔥 CLEAN TEXT
# ============================================================

def normalize_text(text):

    if not text:
        return ""

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# ============================================================
# 🔥 PARAGRAPH BUILDER
# ============================================================

def build_paragraphs(text):

    # ====================================================
    # 🔥 PRIMARY PARAGRAPH SPLIT
    # ====================================================

    paras = re.split(r"\n\s*\n", text)

    # ====================================================
    # 🔥 OCR COLLAPSE RECOVERY
    # ====================================================

    if len(paras) <= 3:

        paras = re.split(

            r'(?<=[\.!?])\s+(?='
            r'(?:we|therefore|thus|hence|accordingly|'
            r'in view of|for the foregoing|appeal|petition|'
            r'the appeal|the petition|ordered accordingly|'
            r'consequently|resultantly|henceforth)'
            r')',

            text,

            flags=re.I
        )

    cleaned = []

    for para in paras:

        para = normalize_text(para)

        if len(para) > 20:

            cleaned.append(para)

    # ====================================================
    # 🔥 FALLBACK SENTENCE WINDOWS
    # ====================================================

    if len(cleaned) <= 2:

        sentences = re.split(
            r'(?<=[\.!?])\s+',
            text
        )

        window = []

        rebuilt = []

        for sent in sentences:

            sent = normalize_text(sent)

            if not sent:
                continue

            window.append(sent)

            if len(window) >= 4:

                rebuilt.append(
                    " ".join(window)
                )

                window = []

        if rebuilt:

            cleaned = rebuilt


    # ====================================================
    # 🔥 HARD FALLBACK PARAGRAPH GUARANTEE
    # ====================================================

    if not cleaned:

        emergency_sentences = re.split(
            r'(?<=[\.\!\?])\s+',
            text
        )

        emergency_sentences = [

            normalize_text(x)

            for x in emergency_sentences

            if normalize_text(x)
        ]

        if emergency_sentences:

            cleaned = [

                " ".join(
                    emergency_sentences[i:i+5]
                )

                for i in range(
                    0,
                    len(emergency_sentences),
                    5
                )
            ]

        print("🔥 EMERGENCY PARAGRAPH FALLBACK ACTIVATED")

        print(len(cleaned))



    return cleaned

# ============================================================
# 🔥 WINNING PARTY INFERENCE
# ============================================================

def infer_winning_party(disposition):

    disposition = disposition.lower()

    if "allowed" in disposition:

        return "Appellant/Petitioner"

    if "dismissed" in disposition:

        return "Respondent"

    if "acquittal" in disposition:

        return "Accused"

    return "Unknown"


# ============================================================
# 🔥 MAIN EXTRACTION ENGINE
# ============================================================

print("🔥🔥🔥 OPERATIVE ENGINE VERSION: MAY24_RUNTIME_SYNC_V1 🔥🔥🔥")

def extract_operative_order(

    full_text,
    semantic_paragraphs=None,
    category=None,
):

    try:

        full_text = normalize_text(full_text)

        if not full_text:

            return {

                "operative_order": [],
                "final_holding": "Unknown",
                "disposition_type": "Unknown",
                "winning_party": "Unknown",
                "operative_para": "para-unknown",
                "confidence": 0,
                "signals": [],
                "contradictions": [],
            }

        # ====================================================
        # 🔥 USE SEMANTIC PARAGRAPHS
        # ====================================================

        if semantic_paragraphs and isinstance(

            semantic_paragraphs,
            list
        ):

            paragraphs = semantic_paragraphs

            print("🔥 USING SEMANTIC PARAGRAPHS")

            print("🔥 SEMANTIC PARAGRAPH COUNT:")

            print(len(paragraphs))

        else:

            paragraphs = build_paragraphs(full_text)

            print("🔥 USING REBUILT PARAGRAPHS")

            print("🔥 REBUILT PARAGRAPH COUNT:")

            print(len(paragraphs))

        # ====================================================
        # 🔥 ENDING TEXT PRIORITY
        # ====================================================

        tail_text = full_text[-25000:]

        disposition_scores = defaultdict(int)

        matched_signals = []

        contradictions = []

        best_paragraph = ""

        best_para_index = -1

        # ====================================================
        # 🔥 PARAGRAPH LEVEL ANALYSIS
        # ====================================================

        for idx, para in enumerate(paragraphs):
            print("🔥 PARA TYPE:")
            print(type(para))

            if isinstance(para, dict):

                para = para.get("paragraph") or para.get("text") or str(para)

            elif isinstance(para, list):

                para = " ".join(map(str, para))

            elif not isinstance(para, str):

                para = str(para)


            para_lower = para.lower()

            # --------------------------------------------
            # 🔥 PROCEDURAL STAGE DETECTION
            # --------------------------------------------

            procedural_stage = None

            try:

                stage_result = detect_procedural_history(
                    para
                )

                if stage_result:

                    procedural_stage = stage_result[0].get(
                        "stage"
                    )

            except Exception as e:

                print("❌ Procedural Stage Detection Error")
                print(str(e))


            print("🔥 PROCEDURAL STAGE:")
            print(procedural_stage)

            paragraph_score = 0

            # ------------------------------------------------
            # 🔥 PROCEDURAL HISTORY PENALTY
            # ------------------------------------------------

            history_indicators = [

                "high court",

                "trial court",

                "sessions judge",

                "learned judge",

                "tribunal",

                "wakf tribunal",

                "civil court",

                "munsif",

                "revision petition",

                "written statement",

                "plaintiff filed",

                "defendant no.",

                "evidence",

                "dw-",

                "pw-",

                "trial",

                "suit was dismissed",

                "high court held",

                "tribunal held",

                "filed this appeal",

                "approached this court",

                "special leave petition",

                "brief facts",

                "case of the prosecution",

                "convicted the appellant",

            ]


            if procedural_stage != "SUPREME_COURT_FINAL":

                if any(

                    indicator in para_lower

                    for indicator in history_indicators
                ):

                    paragraph_score -= 160

            if procedural_stage == "SUPREME_COURT_FINAL":

                paragraph_score += 500

            # ------------------------------------------------
            # 🔥 LOWER COURT DISMISSAL COLLAPSE
            # ------------------------------------------------

            if (

                any(

                    indicator in para_lower

                    for indicator in [

                        "tribunal",

                        "high court",

                        "trial court",

                        "civil court",

                        "sessions judge",

                    ]
                )

                and

                any(

                    word in para_lower

                    for word in [

                        "dismissed",

                        "allowed",

                        "upheld",

                        "decreed",

                    ]
                )
            ):

                paragraph_score -= 220



            # --------------------------------------------
            # POSITION WEIGHT
            # --------------------------------------------

            position_ratio = (

                idx / max(len(paragraphs), 1)
            )

            if position_ratio > 0.92:

                paragraph_score += 150

            elif position_ratio > 0.85:

                paragraph_score += 100

            elif position_ratio > 0.70:

                paragraph_score += 50


            # --------------------------------------------
            # VERB BONUS
            # --------------------------------------------

            for verb in LEGAL_OPERATIVE_VERBS:

                if verb in para_lower:

                    paragraph_score += 10


            # --------------------------------------------
            # 🔥 DISPOSITION SEMANTIC NORMALIZATION
            # --------------------------------------------

            para_lower = re.sub(
                r"\bstand\s+dismissed\b",
                "stands dismissed",
                para_lower
            )

            para_lower = re.sub(
                r"\bappeal\s+dismissed\b",
                "appeal is dismissed",
                para_lower
            )

            para_lower = re.sub(
                r"\bpetition\s+dismissed\b",
                "petition is dismissed",
                para_lower
            )

            para_lower = re.sub(
                r"\bstand\s+allowed\b",
                "stands allowed",
                para_lower
            )

            para_lower = re.sub(
                r"\bappeal\s+allowed\b",
                "appeal is allowed",
                para_lower
            )

            para_lower = re.sub(
                r"\bpetition\s+allowed\b",
                "petition is allowed",
                para_lower
            )

            para_lower = re.sub(
                r"\bno\s+interference\s+called\s+for\b",
                "no interference is called for",
                para_lower
            )

            para_lower = re.sub(
                r"\bdeserve\s+dismissal\b",
                "deserves to be dismissed",
                para_lower
            )




            # --------------------------------------------
            # PATTERN MATCHING
            # --------------------------------------------

            for disposition, patterns in DISPOSITION_PATTERNS.items():

                for pattern in patterns:

                    if re.search(

                        pattern,
                        para_lower,
                        re.IGNORECASE
                    ):

                        # --------------------------------
                        # 🔥 NON-OPERATIVE CONTEXT SUPPRESSION
                        # --------------------------------

                        suppression_terms = [

                            "whether",

                            "candidate",

                            "disclosure",

                            "antecedent",

                            "convicted/acquitted/discharged"
                        ]

                        if any(
                            term in para_lower
                            for term in suppression_terms
                        ):

                            continue

                        score = 80 + paragraph_score

                        # --------------------------------
                        # TAIL TEXT BONUS
                        # --------------------------------

                        tail_window = tail_text.lower()

                        normalized_para = re.sub(
                            r"\s+",
                            " ",
                            para_lower
                        ).strip()

                        normalized_tail = re.sub(
                            r"\s+",
                            " ",
                            tail_window
                        )

                        if (

                            normalized_para[:250] in normalized_tail

                            or

                            any(
                                phrase in normalized_tail
                                for phrase in normalized_para.split(".")[:3]
                                if len(phrase.strip()) > 25
                            )
                        ):

                            score += 30

                        # ------------------------------------------------
                        # 🔥 APPELLATE SUCCESS BOOST
                        # ------------------------------------------------

                        if any(

                            phrase in para_lower

                            for phrase in [

                                "appeal allowed",

                                "appeals are allowed",

                                "we accordingly allow",

                                "impugned judgment set aside",

                                "judgment set aside",

                                "conviction set aside",

                                "order set aside",

                                "order quashed",

                                "proceedings quashed",

                                "petition allowed",

                                "writ petitions are allowed to the extent indicated above",

                                "allowed and set aside"
                            ]
                        ):

                            score += 140

                        # ====================================================
                        # 🔥 HISTORICAL CONTEXT PENALTY
                        # ====================================================

                        historical_hits = sum(

                            1 for marker in HISTORICAL_CONTEXT_MARKERS
                            if marker in para_lower
                        )

                        if historical_hits > 0:

                            score -= (historical_hits * 55)



                        # ------------------------------------------------
                        # 🔥 STRONG DISMISSAL SEMANTIC BOOST
                        # ------------------------------------------------

                        if any(

                            phrase in para_lower

                            for phrase in [

                                "dismissed",

                                "upheld",




                                "no reason to interfere",

                                "courts below",

                                "conviction upheld",
                            ]
                        ):

                            score += 20

                        # ----------------------------------------
                        # 🔥 APPELLATE CONTRADICTION RESOLUTION
                        # ----------------------------------------

                        if (
                            "dismiss" in para_lower
                            and any(
                                x in para_lower
                                for x in [
                                    "allowed",
                                    "set aside",
                                    "quashed"
                                ]
                            )
                        ):

                            score -= 80


                        # ------------------------------------------------
                        # 🔥 SUPREME COURT FINALITY BOOST
                        # ------------------------------------------------

                        finality_indicators = [

                            "we find",

                            "we hold",

                            "we are of the opinion",

                            "no reason to interfere",

                            "appeal deserves",

                            "appeal stands",

                            "ordered accordingly",

                            "accordingly",

                            "thus",

                        ]

                        if any(

                            indicator in para_lower

                            for indicator in finality_indicators
                        ):

                            score += 120



                        # ----------------------------------------
                        # 🔥 JURISPRUDENTIAL PRIORITY WEIGHT
                        # ----------------------------------------

                        weighted_score = score + DISPOSITION_WEIGHTS.get(
                            disposition,
                            50
                        )

                        # Penalize generic disposal if strong
                        # relief language exists

                        if (
                            disposition.lower() == "disposed"
                            and any(
                                strong_word in para_lower
                                for strong_word in [
                                    "allowed",
                                    "quashed",
                                    "set aside",
                                    "acquitted",
                                    "reinstated",
                                    "released",
                                ]
                            )
                        ):

                            weighted_score -= 100

                        disposition_scores[
                            disposition
                        ] += weighted_score

                        print("🔥 WEIGHTED SCORE:")
                        print({
                            "disposition": disposition,
                            "raw_score": score,
                            "weighted_score": weighted_score
                        })
                        print("🔥 DISPOSITION MATCH:")
                        print({
                            "disposition": disposition,
                            "score": score,
                            "paragraph": para[:300]
                        })


                        matched_signals.append({

                            "disposition": disposition,
                            "paragraph": para,
                            "score": score,
                        })

                        # ----------------------------
                        # BEST PARAGRAPH
                        # ----------------------------

                        if score > disposition_scores.get(
                            "BEST_INTERNAL",
                            0
                        ):

                            disposition_scores[
                                "BEST_INTERNAL"
                            ] = score

                            best_paragraph = para

                            best_para_index = idx

        # ====================================================
        # 🔥 CONTRADICTION HANDLING
        # ====================================================

        detected_dispositions = [

            k for k in disposition_scores.keys()
            if k != "BEST_INTERNAL"
        ]

        if len(detected_dispositions) > 1:

            contradictions = detected_dispositions

        # ====================================================
        # 🔥 FINAL HOLDING
        # ====================================================

        final_holding = "Disposition Unknown"

        highest_score = 0

        # ====================================================
        # 🔥 PRIMARY DISPOSITION SCORE PROMOTION
        # ====================================================

        if disposition_scores:

            filtered_scores = {
                k: v
                for k, v in disposition_scores.items()
                if k != "BEST_INTERNAL"
            }

            if filtered_scores:

                final_holding = max(
                    filtered_scores,
                    key=filtered_scores.get
                )

                highest_score = filtered_scores.get(
                    final_holding,
                    0
                )

                print("🔥 PRIMARY DISPOSITION PROMOTED")
                print(final_holding)
                print(highest_score)


        # ====================================================
        # 🔥 SUPREME COURT FINAL OVERRIDE
        # ====================================================

        best_paragraph_lower = best_paragraph.lower()

        print("🔥 BEST PARAGRAPH LOWER:")
        print(best_paragraph_lower)


        # ====================================================
        # 🔥 GENERIC FINAL OPERATIVE FALLBACK
        # ====================================================

        if (

            final_holding == "Disposition Unknown"

            or highest_score <= 0
        ):

            tail_start = max(

                int(len(paragraphs) * 0.80),

                0
            )

            tail_candidates = paragraphs[tail_start:]

            for candidate in reversed(tail_candidates):

                if isinstance(candidate, dict):

                    candidate = candidate.get("paragraph") or candidate.get("text") or ""

                candidate_text = str(candidate).strip()

                candidate_lower = candidate_text.lower()

                if not candidate_text:

                    continue

                if any(

                    indicator in candidate_lower

                    for indicator in history_indicators
                ):

                    print(
                        "❌ OPERATIVE CANDIDATE SUPPRESSED:"
                    )

                    print(candidate_text[:800])

                    continue

                if any(

                    phrase in candidate_lower

                    for phrase in [

                        "we find",

                        "we hold",

                        "accordingly",

                        "thus",

                        "therefore",

                        "ordered accordingly",

                        "no reason to interfere",



                        "interference",

                    ]
                ):

                    if "contempt petition" in candidate_lower:

                        final_holding = "Contempt Petition Disposed"

                    elif "writ petition" in candidate_lower:

                        final_holding = "Writ Petition Disposed"

                    elif "review petition" in candidate_lower:

                        final_holding = "Review Petition Dismissed"

                    elif "slp" in candidate_lower:

                        final_holding = "SLP Dismissed"

                    else:

                        if final_holding == "Disposition Unknown":

                            final_holding = "Appeal Dismissed"

                    disposition_type = final_holding

                    winning_party = "Respondent"

                    para_match = re.match(

                        r"^\s*(\d+)\.",

                        candidate_text
                    )

                    if para_match:

                        operative_para = (
                            f"para-{para_match.group(1)}"
                        )

                    else:

                        operative_para = (
                            f"para-{len(paragraphs)}"
                        )

                    best_paragraph = candidate_text

                    confidence = 85

                    print("🔥 GENERIC FINAL OPERATIVE FALLBACK TRIGGERED")


                    normalized_para = re.sub(
                        r"\s+",
                        " ",
                        re.sub(
                            r"[^a-z0-9]",
                            " ",
                            candidate_text.lower()
                        )
                    ).strip()

                    supreme_positive_markers = [

                        "allow these appeals",

                        "appeals are allowed",

                        "appeal is allowed",

                        "writ petition is allowed",

                        "writ petitions are allowed",

                        "petition is allowed",

                        "petitions are allowed",

                        "rule is made absolute",

                        "impugned order is quashed",

                        "order stands quashed",

                        "allowed to the extent indicated above",

                        "set aside the orders of conviction",

                        "set aside the conviction",

                        "set at liberty",

                        "released forthwith",

                    ]

                    if any(
                        marker in normalized_para
                        for marker in supreme_positive_markers
                    ):

                        print(
                            "🔥 SUPREME COURT FINAL OVERRIDE TRIGGERED"
                        )

                        final_holding = "Appeal Allowed"

                        disposition_type = "Appeal Allowed"

                        winning_party = "Appellant"

                        contradictions = []

                        matched_signals = []

                        disposition_scores = {}

                        return {

                            "operative_order": [],

                            "final_holding": final_holding,

                            "disposition_type": disposition_type,

                            "winning_party": winning_party,

                            "operative_para": operative_para,

                            "paragraph": candidate_text,

                            "confidence": 95,

                            "signals": [],

                            "contradictions": []

                        }

                    print(candidate_text[:500])

                    break


        # ====================================================
        confidence = 0

        # 🔥 CONFIDENCE
        # ====================================================

        if highest_score > 0:

            confidence = min(

                highest_score,

                100
            )

        # ====================================================
        # 🔥 WINNING PARTY
        # ====================================================

        winning_party = infer_winning_party(
            final_holding
        )

        # ====================================================
        # 🔥 OPERATIVE SIGNAL DEDUP ENGINE
        # ====================================================

        seen_operatives = set()

        deduped_signals = []

        for sig in matched_signals:

            if not isinstance(sig, dict):
                continue

            para = sig.get(
                "paragraph",
                ""
            ).strip().lower()

            if not para:
                continue

            if para in seen_operatives:
                continue

            seen_operatives.add(para)

            deduped_signals.append(sig)

        matched_signals = deduped_signals

        # ====================================================
        # 🔥 RESULT
        # ====================================================

        result = {

            "operative_order": matched_signals,

            "final_holding": final_holding,

            "disposition_type": final_holding,

            "winning_party": winning_party,

            "operative_para": (

                operative_para
                if "operative_para" in locals()
                else (
                    f"para-{best_para_index + 1}"
                    if best_para_index >= 0
                    else "para-unknown"
                )
            ),

            "paragraph": best_paragraph,

            "confidence": confidence,

            "signals": matched_signals,

            "contradictions": contradictions,
        }

        print("✅ Operative Order Extracted:")
        print(result)

        return result

    except Exception as e:

        print("❌ OPERATIVE ORDER ENGINE ERROR:")
        print(str(e))

        return {

            "operative_order": [],
            "final_holding": "Disposition Unknown",
            "disposition_type": "Unknown",
            "winning_party": "Unknown",
            "operative_para": "para-unknown",
            "confidence": 0,
            "signals": [],
            "contradictions": [str(e)],
        }
