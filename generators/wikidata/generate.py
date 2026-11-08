"""wikidata: the academic conferences, conference series and proceedings of Wikidata, true to the source.

Source: inputs:wikidata/<date>, the answers of QLever's complete Wikidata (harvest.py): 35,271 items selected as
academic conferences or workshops (P31/P279* Q2020153), academic conference series (P31/P279* Q47258130), items with
an identifier of a conference or a series (dblp venue and event, WikiCFP event and series, KISTI, ACM conference and
event) or proceedings of an event (P4745); every truthy statement (wdt:), and the labels, aliases and descriptions in
English, German and the default for all languages (mul). CC0.

The statements are kept as Wikidata states them, with Wikidata's IRIs (items http://www.wikidata.org/entity/Q…);
IRIs of known sources in canonical form. The items these statements name (places, organisers, subjects) are not
described here.
"""

from cr import iris

INPUTS = {"harvest": "inputs:wikidata/2026-11-08"}
PARAMS = {}

FILES = ["statements.nt", "labels.nt", "aliases.nt", "descriptions.nt"]


def generate(run):
    def data():
        for name in FILES:
            n = 0
            for t in run.triples("harvest", file=name):
                n += 1
                yield t
            run.log(f"{name}: {n:,} statements")

    run.write_turtle("wikidata.ttl.gz", iris.canonical_triples(data()))
