# =========================================================
# 🔥 JURISPRUDENTIAL CONSENSUS ENGINE
# =========================================================

from collections import defaultdict

# =========================================================
# 🔥 CONSENSUS STATE
# =========================================================

JURISPRUDENTIAL_CONSENSUS = {

    "doctrine_votes": defaultdict(list),

    "consensus_results": {},

    "consensus_events": [],

    "global_equilibrium_score": 1.0,

    "consensus_mode": "PLANETARY_CONSENSUS"
}

# =========================================================
# 🔥 REGISTER DOCTRINE VOTE
# =========================================================

def register_doctrine_vote(

    federation_name,
    doctrine_name,
    doctrine_weight
):

    JURISPRUDENTIAL_CONSENSUS[
        "doctrine_votes"
    ][doctrine_name].append({

        "federation":
            federation_name,

        "weight":
            round(doctrine_weight, 2)
    })

    return True

# =========================================================
# 🔥 BUILD CONSENSUS
# =========================================================

def build_doctrinal_consensus():

    results = {}

    equilibrium_scores = []

    try:

        for doctrine, votes in (
            JURISPRUDENTIAL_CONSENSUS[
                "doctrine_votes"
            ].items()
        ):

            if not votes:

                continue

            total_weight = sum(
                v["weight"]
                for v in votes
            )

            avg_weight = round(

                total_weight / len(votes),

                2
            )

            spread = round(

                max(v["weight"] for v in votes)
                -
                min(v["weight"] for v in votes),

                2
            )

            consensus_strength = round(
                1 - spread,
                2
            )

            equilibrium_scores.append(
                consensus_strength
            )

            results[doctrine] = {

                "average_weight":
                    avg_weight,

                "consensus_strength":
                    consensus_strength,

                "participating_federations":
                    len(votes),

                "stable":
                    consensus_strength >= 0.60
            }

            JURISPRUDENTIAL_CONSENSUS[
                "consensus_events"
            ].append({

                "doctrine":
                    doctrine,

                "consensus_strength":
                    consensus_strength
            })

        if equilibrium_scores:

            global_score = round(

                sum(equilibrium_scores)
                /
                len(equilibrium_scores),

                2
            )

            JURISPRUDENTIAL_CONSENSUS[
                "global_equilibrium_score"
            ] = global_score

        JURISPRUDENTIAL_CONSENSUS[
            "consensus_results"
        ] = results

    except Exception as e:

        print(
            "❌ CONSENSUS ENGINE ERROR:"
        )

        print(str(e))

    return results

# =========================================================
# 🔥 FETCH CONSENSUS STATE
# =========================================================

def get_consensus_state():

    return JURISPRUDENTIAL_CONSENSUS
