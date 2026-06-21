BLACKLIST = {

    "relief granted",
    "relief denied",

    "criminal appeal allowed",

    "appellate interference",

    "tribunal adjudication",

    "election commission compliance",

    "electoral transparency"

    "amendment) act, 2015",
    "tax act, 1961",
    "ia of the income tax act, 1961",
    "b) of the central excise act, 1944",
    "d) of the prevention of corruption act, 1988",
    "land and traffic) act, 2002",
    "finance act, 1994",
    "finance act, 2007",
    "finance act, 2012",
    "draft rules, 2020",
}


def is_blacklisted(value):

    if not value:
        return False

    return value.strip().lower() in BLACKLIST
