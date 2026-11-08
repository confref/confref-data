"""Harvest the conference part of dblp from its SPARQL endpoint (the input of the generator).

python3 generators/dblp/harvest.py <out dir>

The queries (QUERIES) run against https://sparql.dblp.org/sparql (QLever, the current dblp release); each is saved as
<name>.rq beside its answer, unchanged (<name>.nt for CONSTRUCT, <name>.tsv for SELECT). harvest.json records the
endpoint, the times and the Last-Modified date of the dblp RDF dump at that time (the endpoint states no version).
The full dump (dblp.ttl.gz, 2.4 GB) is not needed for the conference part. Blank nodes are not constructed: the
typed identifiers (datacite:hasIdentifier) come as rows (identifiers.tsv), the authorship signatures are not
harvested (persons come later).
"""

import datetime
import json
import sys
import urllib.parse
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from cr.fetch import get, request  # noqa: E402

ENDPOINT = "https://sparql.dblp.org/sparql"
DUMP = "https://dblp.org/rdf/dblp.ttl.gz"
PREFIXES = """PREFIX dblp: <https://dblp.org/rdf/schema#>
PREFIX datacite: <http://purl.org/spar/datacite/>
PREFIX litre: <http://purl.org/spar/literal/>
"""
# the conference proceedings: editorships published in a conference stream
PROCEEDINGS = "?e a dblp:Editorship ; dblp:publishedInStream ?c . ?c a dblp:Conference ."
QUERIES = {
    "conference-streams": ("construct", """CONSTRUCT { ?s ?p ?o } WHERE {
  ?s a dblp:Conference ; ?p ?o . FILTER(!isBlank(?o)) }"""),
    "proceedings": ("construct", f"""CONSTRUCT {{ ?e ?p ?o }} WHERE {{
  {{ SELECT DISTINCT ?e WHERE {{ {PROCEEDINGS} }} }}
  ?e ?p ?o . FILTER(!isBlank(?o)) }}"""),
    "other-streams": ("construct", f"""CONSTRUCT {{ ?t ?p ?o }} WHERE {{
  {{ SELECT DISTINCT ?t WHERE {{ {PROCEEDINGS} ?e dblp:publishedInStream ?t . FILTER NOT EXISTS {{ ?t a dblp:Conference }} }} }}
  ?t ?p ?o . FILTER(!isBlank(?o)) }}"""),
    "identifiers": ("select", f"""SELECT DISTINCT ?s ?scheme ?value WHERE {{
  {{ ?s a dblp:Conference }} UNION
  {{ SELECT DISTINCT ?s WHERE {{ ?s a dblp:Editorship ; dblp:publishedInStream ?c . ?c a dblp:Conference }} }} UNION
  {{ SELECT DISTINCT ?s WHERE {{ {PROCEEDINGS} ?e dblp:publishedInStream ?s . FILTER NOT EXISTS {{ ?s a dblp:Conference }} }} }}
  ?s datacite:hasIdentifier ?b . ?b datacite:usesIdentifierScheme ?scheme ; litre:hasLiteralValue ?value }}"""),
}
ACCEPT = {"construct": "application/n-triples", "select": "text/tab-separated-values"}
SUFFIX = {"construct": ".nt", "select": ".tsv"}


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    with urllib.request.urlopen(request(DUMP, method="HEAD"), timeout=60) as r:
        dump_modified = r.headers.get("Last-Modified")
    report = {"endpoint": ENDPOINT, "dump_last_modified": dump_modified, "started": now(), "queries": {}}
    for name, (kind, query) in QUERIES.items():
        q = PREFIXES + query + "\n"
        (out / f"{name}.rq").write_text(q, encoding="utf-8")
        path = out / (name + SUFFIX[kind])
        if not path.exists():
            t = now()
            body = get(ENDPOINT + "?" + urllib.parse.urlencode({"query": q}),
                       headers={"Accept": ACCEPT[kind]}, timeout=1200)
            path.write_bytes(body)
            report["queries"][name] = {"time": t, "bytes": len(body), "lines": body.count(b"\n")}
            print(name, report["queries"][name], flush=True)
    report["finished"] = now()
    (out / "harvest.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
