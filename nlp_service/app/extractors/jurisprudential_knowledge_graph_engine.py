
from app.legal_ontology.canonical_legal_object_engine import (

    canonicalize_act_name,
    canonicalize_point_of_law,
    build_canonical_legal_object
)

# =========================================================
# 🔥 JURISPRUDENTIAL KNOWLEDGE GRAPH ENGINE
# =========================================================


def build_jurisprudential_knowledge_graph(

    case_number=None,
    judges=None,
    acts=None,
    sections=None,
    dominant_issue=None,
    ratio_data=None,
    operative_data=None,
    temporal_data=None
):

    try:

        graph = {

            "nodes": [],

            "edges": [],

            "summary": {},

            "confidence": 0
        }

        # -------------------------------------------------
        # CASE NODE
        # -------------------------------------------------

        case_id = "Unknown Case"

        if isinstance(case_number, dict):

            # ---------------------------------------------
            # 🔒 IMMUTABLE GRAPH CASE IDENTITY
            # ---------------------------------------------

            case_id = case_number.get(
                "canonical_id"
            )

            if not case_id:

                case_id = case_number.get(
                    "case_number",
                    "Unknown Case"
                )

        assert case_id is not None

        assert str(case_id).strip() != ""

        # ---------------------------------------------
        # 🔒 GRAPH INTEGRITY ASSERTION LOCK
        # ---------------------------------------------

        assert case_id is not None

        assert str(case_id).strip() != ""

        graph["nodes"].append({

            "id":
                case_id,

            "type":
                "CASE"
        })

        # -------------------------------------------------
        # JUDGE NODES
        # -------------------------------------------------

        if not isinstance(judges, list):

            judges = []

        for judge in judges:

            graph["nodes"].append({

                "id":
                    judge,

                "type":
                    "JUDGE"
            })

            graph["edges"].append({

                "source":
                    case_id,

                "target":
                    judge,

                "relation":
                    "DECIDED_BY"
            })

        # -------------------------------------------------
        # ACT NODES
        # -------------------------------------------------

        if isinstance(acts, list):

            for act in acts:

                canonical_act = (
                    canonicalize_act_name(
                        act
                    )
                )

                canonical_act_object = (
                    build_canonical_legal_object(
                        canonical_act,
                        "ACT"
                    )
                )

                graph["nodes"].append({

                    "id":
                        canonical_act_object.get(
                            "id"
                        ),

                    "label":
                        canonical_act,

                    "type":
                        "ACT"
                })

                graph["edges"].append({

                    "source":
                        case_id,

                    "target":
                        act,

                    "relation":
                        "INVOLVES_ACT"
                })

        # -------------------------------------------------
        # SECTION NODES
        # -------------------------------------------------

        if isinstance(sections, dict):

            section_items = sections.get(
                "sections",
                []
            )

            for item in section_items:

                section_name = item.get(
                    "section"
                )

                if not section_name:

                    continue

                graph["nodes"].append({

                    "id":
                        section_name,

                    "type":
                        "SECTION"
                })

                graph["edges"].append({

                    "source":
                        case_id,

                    "target":
                        section_name,

                    "relation":
                        "INVOLVES_SECTION"
                })

        # -------------------------------------------------
        # DOMINANT ISSUE
        # -------------------------------------------------

        if isinstance(dominant_issue, dict):

            issue = dominant_issue.get(
                "dominant_issue"
            )

            if issue:

                canonical_issue = (
                    canonicalize_point_of_law(
                        issue
                    )
                )

                canonical_issue_object = (
                    build_canonical_legal_object(
                        canonical_issue,
                        "POINT_OF_LAW"
                    )
                )

                graph["nodes"].append({

                    "id":
                        canonical_issue_object.get(
                            "id"
                        ),

                    "label":
                        canonical_issue,

                    "type":
                        "DOCTRINE"
                })

                graph["edges"].append({

                    "source":
                        case_id,

                    "target":
                        issue,

                    "relation":
                        "INVOLVES_DOCTRINE"
                })

        # -------------------------------------------------
        # OPERATIVE HOLDING
        # -------------------------------------------------

        if isinstance(operative_data, dict):

            holding = operative_data.get(
                "final_holding"
            )

            if holding:

                graph["nodes"].append({

                    "id":
                        holding,

                    "type":
                        "OUTCOME"
                })

                graph["edges"].append({

                    "source":
                        case_id,

                    "target":
                        holding,

                    "relation":
                        "RESULTED_IN"
                })

        # -------------------------------------------------
        # TEMPORAL DOCTRINES
        # -------------------------------------------------

        if isinstance(temporal_data, dict):

            doctrines = temporal_data.get(
                "doctrinal_movements",
                []
            )

            for item in doctrines:

                doctrine = item.get(
                    "doctrine"
                )

                if doctrine:

                    graph["nodes"].append({

                        "id":
                            doctrine,

                        "type":
                            "TEMPORAL_DOCTRINE"
                    })

                    graph["edges"].append({

                        "source":
                            case_id,

                        "target":
                            doctrine,

                        "relation":
                            "EVOLVES_DOCTRINE"
                    })

        # -------------------------------------------------
        # REMOVE DUPLICATES
        # -------------------------------------------------

        unique_nodes = []

        seen_nodes = set()

        for node in graph["nodes"]:

            key = (

                node.get("id"),

                node.get("type")
            )

            if key not in seen_nodes:

                seen_nodes.add(key)

                unique_nodes.append(node)

        graph["nodes"] = unique_nodes

        # -------------------------------------------------
        # SUMMARY
        # -------------------------------------------------

        graph["summary"] = {

            "total_nodes":
                len(graph["nodes"]),

            "total_edges":
                len(graph["edges"])
        }

        graph["confidence"] = min(

            95,

            50 + len(graph["edges"])
        )

        print(
            "✅ Jurisprudential Knowledge Graph:"
        )

        print(graph)

        return graph

    except Exception as e:

        print(
            "❌ Knowledge Graph Error:",
            str(e)
        )

        return {

            "nodes": [],

            "edges": [],

            "summary": {},

            "confidence": 0
        }
