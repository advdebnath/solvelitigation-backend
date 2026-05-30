def build_issue_hierarchy(issues):

    if not issues:
        return {}

    hierarchy = {
        "main_issue": issues[0],
        "sub_issues": issues[1:5],
        "procedural_issues": [],
        "constitutional_issues": [],
    }

    for issue in issues:

        issue_type = issue.get("issueType", "")

        if issue_type in ["jurisdiction", "limitation", "natural_justice"]:
            hierarchy["procedural_issues"].append(issue)

    return hierarchy
