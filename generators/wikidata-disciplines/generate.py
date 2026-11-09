"""wikidata-disciplines: the Wikidata items that ls-fields names as disciplines, with their labels, true to the source
(decision 0019).

Source: inputs:wikidata/fields-2026-11-09 (generators/ls-fields/harvest.py, QLever's complete Wikidata): the labels in
English, German and for all languages (mul) of every item that ls-fields links to as a discipline (cr:discipline).
CC0.
"""

from cr.rdf import IRI, read_triples

INPUTS = {"harvest": "inputs:wikidata/fields-2026-11-09/wikidata-fields-2026-11-09/labels.nt",
          "links": "ls-fields/2026-11-09"}
PARAMS = {}

DISCIPLINE = "https://id.confref.org/ontology/discipline"


def generate(run):
    items = {str(o) for _s, p, o in run.triples("links") if p == DISCIPLINE}
    out = {(s, p, o) for s, p, o in read_triples(run.input("harvest")) if str(s) in items}
    missing = items - {str(s) for s, _p, _o in out}
    run.note(f"{len(items):,} disciplines named by ls-fields; {len(missing):,} without a label in the harvest.")
    run.write_turtle("wikidata-disciplines.ttl.gz", out)
