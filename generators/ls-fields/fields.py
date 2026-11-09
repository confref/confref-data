"""The academic fields (OECD FOS 2007, dataset oecd-fos) and disciplines (Wikidata items) of the sources (shared by
the harvest and the generator of ls-fields; decision 0019).

ANCHORS: Wikidata items that stand for an OECD field (or a major field); a discipline item that is one of them, or a
direct subclass or part of one of them in Wikidata (wdt:P279, wdt:P361, one step), falls under that field.
PORTAL_AREAS: the 27 research areas of the confref portal (the subject areas of Springer) with their field and
discipline. BOOK_SERIES: the Springer book series of proceedings with the field of the conferences they publish.
"""

import re

ANCHORS = {   # Wikidata item -> OECD FOS code
    "Q7991": "1", "Q395": "1.1", "Q21198": "1.2", "Q16387": "1.2", "Q11660": "1.2", "Q80993": "1.2",
    "Q413": "1.3", "Q2329": "1.4", "Q188847": "1.5", "Q420": "1.6",
    "Q11023": "2", "Q77590": "2.1", "Q43035": "2.2", "Q101333": "2.3", "Q83588": "2.4", "Q228736": "2.5",
    "Q327092": "2.6", "Q146326": "2.7", "Q11468": "2.10",
    "Q11190": "3",
    "Q3606845": "4", "Q11451": "4.1", "Q170201": "4.3",
    "Q34749": "5", "Q9418": "5.1", "Q8134": "5.2", "Q4830453": "5.2", "Q8434": "5.3", "Q21201": "5.4",
    "Q7748": "5.5", "Q36442": "5.6", "Q12831143": "5.7", "Q187097": "5.7", "Q165650": "5.8", "Q11680831": "5.8",
    "Q80083": "6", "Q309": "6.1", "Q23498": "6.1", "Q8162": "6.2", "Q8242": "6.2", "Q5891": "6.3", "Q9465": "6.3",
    "Q34187": "6.3", "Q735": "6.4", "Q50637": "6.4", "Q184485": "6.4", "Q638": "6.4",
}
# classes of disciplines in Wikidata: academic discipline, field of study / specialty, branch of science
DISCIPLINE_CLASSES = ["Q11862829", "Q1047113", "Q2465832"]

PORTAL_AREAS = {   # label -> (OECD FOS codes, Wikidata item)
    "Computer Science": (["1.2"], "Q21198"),
    "Engineering": (["2"], "Q11023"),
    "Mathematics": (["1.1"], "Q395"),
    "Business and Management": (["5.2"], "Q4830453"),
    "Physics": (["1.3"], "Q413"),
    "Life Sciences": (["1.6"], "Q420"),
    "Materials Science": (["2.5"], "Q228736"),
    "Economics": (["5.2"], "Q8134"),
    "Energy": (["2"], None),
    "Earth Sciences": (["1.5"], None),
    "Statistics": (["1.1"], "Q12483"),
    "Medicine & Public Health": (["3"], "Q11190"),
    "Environment": (["1.5"], "Q188847"),
    "Chemistry": (["1.4"], "Q2329"),
    "Social Sciences": (["5"], "Q34749"),
    "Geography": (["1.5", "5.7"], "Q1071"),
    "Biomedicine": (["3.1"], None),
    "Psychology": (["5.1"], "Q9418"),
    "Linguistics": (["6.2"], "Q8162"),
    "Education": (["5.3"], "Q8434"),
    "Science, Humanities and Social Sciences, multidisciplinary": ([], None),
    "Political Science and International Relations": (["5.6"], "Q36442"),
    "History": (["6.1"], "Q309"),
    "Finance": (["5.2"], "Q43015"),
    "Criminology and Criminal Justice": (["5.4"], "Q161733"),
    "Climate": (["1.5"], None),
    "Architecture / Design": (["6.4"], "Q12271"),
}

BOOK_SERIES = {   # spr:bookSeriesAcronym -> OECD FOS codes
    "LNCS": ["1.2"], "LNAI": ["1.2"], "LNBI": ["1.2", "1.6"], "CCIS": ["1.2"], "LNBIP": ["1.2", "5.2"],
    "IFIP-AICT": ["1.2"], "LNICST": ["1.2"], "AISC": ["1.2"], "SCI": ["1.2"], "LNEE": ["2.2"],
    "LNNS": ["1.2"], "SIST": ["1.2"], "IFMBE": ["2.6"], "SPPHY": ["1.3"], "PROMS": ["1.1"], "SPMS": ["1.1"],
    "LNCE": ["2.1"], "LNME": ["2.3"], "LNDECT": ["1.2"], "EAI/Springer Innovations in Communication and Computing": ["1.2"],
}

# ConfIDent's names of the OECD fields ("Computer And Information Sciences") -> code, by the key below
def key(name):
    return re.sub(r"[^a-z]+", " ", (name or "").lower()).strip()
