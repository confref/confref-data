"""wikidata-places: the Wikidata items that ls-places names as the places of events, and their countries, true to
the source (decision 0018).

Source: inputs:wikidata/places-2026-11-09 (generators/ls-places/harvest.py, QLever's complete Wikidata): of every
item that ls-places links to, the truthy statements wdt:P17 (country), P625 (coordinates, as Wikidata gives them:
"Point(<longitude> <latitude>)"^^geo:wktLiteral), P31 (instance of), P131 (located in), P297 and P300 (ISO codes),
P1082 (population) and the labels in English, German and for all languages (mul); of their countries the ISO code
(P297) and the labels in these languages. CC0.
"""

from cr.rdf import IRI, read_triples

INPUTS = {"harvest": "inputs:wikidata/places-2026-11-09", "links": "ls-places/2026-11-09"}
PARAMS = {}

W = "http://www.wikidata.org/prop/direct/"
RDFS_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
LANGS = {"en", "de", "mul"}


def harvest_file(run, name):
    for p in run.inputs("harvest"):
        if p.name == name:
            return p
    raise FileNotFoundError(name)


def generate(run):
    places = {str(o) for _s, _p, o in run.triples("links")}
    out = set()
    countries = set()
    for s, p, o in read_triples(harvest_file(run, "statements.nt")):
        if str(s) not in places:
            continue
        if p == RDFS_LABEL and o.lang not in LANGS:
            continue
        out.add((s, p, o))
        if p == W + "P17":
            countries.add(str(o))
    countries |= {x for x in places if x in countries}
    for f in ("countries.nt", "country-labels.nt"):
        for s, p, o in read_triples(harvest_file(run, f)):
            if str(s) in countries and (p != RDFS_LABEL or o.lang in LANGS):
                out.add((s, p, o))
    missing = places - {str(s) for s, _p, _o in out}
    run.note(f"{len(places):,} places linked by ls-places, {len(countries):,} countries; "
             f"{len(missing):,} linked items without statements in the harvest.")
    run.write_turtle("wikidata-places.ttl.gz", out)
