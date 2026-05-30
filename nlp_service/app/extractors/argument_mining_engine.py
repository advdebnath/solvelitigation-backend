import re

# =========================================================
# 🔥 ARGUMENT PATTERNS
# =========================================================

ARGUMENT_PATTERNS = {
    "Petitioner": [
        r"learned counsel for the petitioner submitted",
        r"petitioner contended",
        r"petitioner argued",
        r"it was submitted on behalf of the petitioner",
        r"counsel appearing for the petitioner",
    ],
    "Respondent": [
        r"learned counsel for the respondent submitted",
        r"respondent contended",
        r"respondent argued",
        r"it was submitted on behalf of the respondent",
        r"counsel appearing for the respondent",
    ],
}


# =========================================================
# 🔥 ACCEPTANCE
# =========================================================

ACCEPT_PATTERNS = [
    r"we agree",
    r"submission deserves acceptance",
    r"contention is accepted",
    r"argument is accepted",
    r"correctly submitted",
    r"has merit",
]


# =========================================================
# 🔥 REJECTION
# =========================================================

REJECT_PATTERNS = [
    r"cannot be accepted",
    r"submission is rejected",
    r"without merit",
    r"contention fails",
    r"argument fails",
    r"we do not agree",
]


# =========================================================
# 🔥 CLEAN
# =========================================================


def clean_text(text):

    text = re.sub(r"\s+", " ", text)

    return text.strip()


# =========================================================
# 🔥 DETECT STATUS
# =========================================================


def detect_argument_status(context):

    for pattern in ACCEPT_PATTERNS:

        if re.search(pattern, context, re.I):

            return "Accepted"

    for pattern in REJECT_PATTERNS:

        if re.search(pattern, context, re.I):

            return "Rejected"

    return "Neutral"


# =========================================================
# 🔥 SPLIT SENTENCES
# =========================================================


def split_sentences(text):

    return re.split(r"(?<=[.!?])\s+", text)


# =========================================================
# 🔥 EXTRACT ARGUMENTS
# =========================================================


def extract_arguments(text):

    try:

        text = clean_text(text)

        sentences = split_sentences(text)

        arguments = []

        # =================================================
        # 🔥 PROCESS SENTENCES
        # =================================================

        for idx, sentence in enumerate(sentences):

            lower = sentence.lower()

            role = None

            # =============================================
            # 🔥 DETECT PARTY
            # =============================================

            for label, patterns in ARGUMENT_PATTERNS.items():

                matched = False

                for pattern in patterns:

                    if re.search(pattern, lower, re.I):

                        role = label
                        matched = True
                        break

                if matched:
                    break

            if not role:
                continue

            # =============================================
            # 🔥 LOCAL CONTEXT ONLY
            # =============================================

            local_context = " ".join(sentences[idx : min(len(sentences), idx + 2)])

            local_context = clean_text(local_context)

            # =============================================
            # 🔥 STATUS
            # =============================================

            status = detect_argument_status(local_context)

            arguments.append(
                {
                    "party": role,
                    "argument": clean_text(sentence),
                    "status": status,
                    "context": local_context[:1000],
                }
            )

        # =================================================
        # 🔥 REMOVE DUPLICATES
        # =================================================

        unique = []

        seen = set()

        for item in arguments:

            key = (item["party"].lower(), item["argument"].lower())

            if key in seen:
                continue

            seen.add(key)

            unique.append(item)

        # =================================================
        # 🔥 RESULT
        # =================================================

        result = {"arguments": unique, "confidence": 95}

        print("✅ Argument Mining Extracted:")

        print(result)

        return result

    except Exception as e:

        print("❌ Argument Mining Error:", str(e))

        return {"arguments": [], "confidence": 0}


# =========================================================
# 🔥 TEST
# =========================================================

if __name__ == "__main__":

    sample = """

    Learned counsel for the petitioner submitted
    that the Wakf property could not be alienated.

    We agree with the submission.

    Learned counsel for the respondent argued
    that tenancy was legally surrendered.

    The contention cannot be accepted.
    """

    print(extract_arguments(sample))
