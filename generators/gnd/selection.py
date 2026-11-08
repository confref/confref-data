"""The GND records confref takes (shared by harvest.py and generate.py): the GND numbers our datasets name.

Seeds: every GND IRI in the stable versions of springer-lod (hasGNDID), dblp and wikidata (as IRI), and every GND
number of wikidata as a literal (P227, the GND ID). One step further (follow): the records that a selected record
names as its place (gndo:placeOfConferenceOrEvent) or as a related conference or event (preceding, succeeding,
hierarchically superior). This is not the full cascade of judaicalink-data (0029); that comes with the identity
layer.
"""

import re

from cr.rdf import Literal, read_triples

SOURCES = ["springer-lod", "dblp", "wikidata"]
GND = re.compile(r"^https?://d-nb\.info/gnd/([0-9][0-9X-]*)$")
P227 = "http://www.wikidata.org/prop/direct/P227"
GNDO = "https://d-nb.info/standards/elementset/gnd#"
FOLLOW = [GNDO + p for p in ("placeOfConferenceOrEvent", "precedingConferenceOrEvent", "succeedingConferenceOrEvent",
                             "hierarchicalSuperiorOfTheConferenceOrEvent", "hierarchicalSuperior")]


def seeds(paths):
    """{GND number: set of datasets} from the data files {slug: [paths]}."""
    found = {}
    for slug, files in paths.items():
        for path in files:
            for _s, p, o in read_triples(path):
                if isinstance(o, Literal):
                    n = o.value if p == P227 else None
                else:
                    m = GND.match(o)
                    n = m.group(1) if m else None
                if n:
                    found.setdefault(n, set()).add(slug)
    return found


def followed(triples):
    """The GND numbers that the given triples name by a FOLLOW property."""
    out = set()
    for s, p, o in triples:
        if p in FOLLOW and isinstance(o, str):
            m = GND.match(o)
            if m:
                out.add(m.group(1))
    return out
