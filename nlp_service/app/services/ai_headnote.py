def generate_ai_headnote(text):
    try:
        text = text[:20000]  # limit size

        # 🔥 simple intelligent extraction
        lines = text.split("\n")

        issue = ""
        decision = ""

        for line in lines[:200]:
            l = line.lower()

            if "whether" in l and not issue:
                issue = line.strip()

            if "held" in l or "allowed" in l or "dismissed" in l:
                decision = line.strip()

        # fallback logic
        if not issue:
            issue = "Legal issue involves interpretation of statutory provisions"

        if not decision:
            decision = "Decision based on facts and applicable law"

        return f"{issue} – {decision}"

    except Exception as e:
        return f"AI headnote error: {str(e)}"
