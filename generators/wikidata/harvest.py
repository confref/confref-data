"""Harvest the conferences, conference series and proceedings of Wikidata (the input of the generator).

python3 generators/wikidata/harvest.py <out dir>

The selection (SELECTION): every item that is an academic conference (P31/P279* Q2020153, workshops included) or an
academic conference series (P31/P279* Q47258130), that carries an identifier of a conference or series (dblp venue
P8926, dblp event P10692, WikiCFP event P5124 and series P5127, KISTI conference P14000, ACM conference P7979 and
event P3333), or that is the proceedings of an event (P4745). Of these items: every truthy statement (wdt:), and the
labels, aliases and descriptions in English, German and the default for all languages (mul).

The queries run against QLever's complete Wikidata (https://qlever.dev/api/wikidata, the dump of 2026-08 with live
updates; the full graph, not split into a scholarly part as the Wikidata Query Service is); each is saved as
<name>.rq beside its answer (<name>.nt). harvest.json records the endpoint, its description of the index and the
times.
"""

import datetime
import json
import sys
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from cr.fetch import get  # noqa: E402

ENDPOINT = "https://qlever.dev/api/wikidata"
PREFIXES = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX schema: <http://schema.org/>
"""
SELECTION = """{ SELECT DISTINCT ?i WHERE {
    { ?i wdt:P31/wdt:P279* wd:Q2020153 } UNION { ?i wdt:P31/wdt:P279* wd:Q47258130 } UNION
    { VALUES ?id { wdt:P8926 wdt:P10692 wdt:P5124 wdt:P5127 wdt:P14000 wdt:P7979 wdt:P3333 wdt:P4745 } ?i ?id ?x } } }"""
LANGUAGES = '"en", "de", "mul"'
QUERIES = {
    "statements": f"""CONSTRUCT {{ ?i ?p ?o }} WHERE {{ {SELECTION}
  ?i ?p ?o . FILTER(STRSTARTS(STR(?p), "http://www.wikidata.org/prop/direct/")) }}""",
    "labels": f"""CONSTRUCT {{ ?i rdfs:label ?l }} WHERE {{ {SELECTION}
  ?i rdfs:label ?l . FILTER(LANG(?l) IN ({LANGUAGES})) }}""",
    "aliases": f"""CONSTRUCT {{ ?i skos:altLabel ?l }} WHERE {{ {SELECTION}
  ?i skos:altLabel ?l . FILTER(LANG(?l) IN ({LANGUAGES})) }}""",
    "descriptions": f"""CONSTRUCT {{ ?i schema:description ?l }} WHERE {{ {SELECTION}
  ?i schema:description ?l . FILTER(LANG(?l) IN ({LANGUAGES})) }}""",
}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    stats = json.loads(get(ENDPOINT + "?cmd=stats"))
    report = {"endpoint": ENDPOINT, "index": stats.get("name-index"), "started": now(), "queries": {}}
    for name, query in QUERIES.items():
        q = PREFIXES + query + "\n"
        (out / f"{name}.rq").write_text(q, encoding="utf-8")
        path = out / f"{name}.nt"
        if not path.exists():
            t = now()
            body = get(ENDPOINT + "?" + urllib.parse.urlencode({"query": q}),
                       headers={"Accept": "application/n-triples"}, timeout=1200)
            path.write_bytes(body)
            report["queries"][name] = {"time": t, "bytes": len(body), "lines": body.count(b"\n")}
            print(name, report["queries"][name], flush=True)
    report["finished"] = now()
    (out / "harvest.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
