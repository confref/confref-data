"""Harvest the Wikidata places that the place names and items of our sources can stand for (the input of ls-places
and wikidata-places).

python3 generators/ls-places/harvest.py <out dir>

1. countries: the items with an ISO 3166-1 code (wdt:P297), with their labels and aliases; subdivisions: the items
   with an ISO 3166-2 code (wdt:P300), with their country, labels and aliases.
2. The place names of the stable versions of the source datasets (places.py, read from the store) are looked up as
   labels and as aliases in LANGUAGES: every item with that label or alias that has coordinates (wdt:P625) and a
   country (wdt:P17) is a candidate (names-labels.tsv, names-aliases.tsv: name, language, item).
3. The facts of the candidates and of the items the sources name as places (wdt:P276, the Wikidata items of GND
   places): candidates.tsv (item, sitelinks, settlement: an instance of a subclass of human settlement Q486972) and
   statements.nt (wdt:P17, P625, P31, P131, P297, P300, P1082 and the labels in en, de, mul).

The queries run against QLever's complete Wikidata (https://qlever.dev/api/wikidata), by POST; each is saved as
<name>.rq (for the batched queries, the first batch) beside its answer. harvest.json records the endpoint, its index,
the datasets read and the times. Labels and aliases are asked in separate queries (a UNION of both times out).
"""

import datetime
import json
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cr import catalog, config  # noqa: E402
from cr.fetch import get, request  # noqa: E402
from cr.rdf import read_triples  # noqa: E402
import places  # noqa: E402

ENDPOINT = "https://qlever.dev/api/wikidata"
PREFIXES = """PREFIX wd: <http://www.wikidata.org/entity/>
PREFIX wdt: <http://www.wikidata.org/prop/direct/>
PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
PREFIX skos: <http://www.w3.org/2004/02/skos/core#>
PREFIX wikibase: <http://wikiba.se/ontology#>
"""
LANGUAGES = ["en", "mul", "de", "fr", "es", "it", "pt", "nl", "pl"]
LABEL_LANGUAGES = '"en", "de", "mul"'
SOURCES = {"springer": "springer-lod", "portal": "confref-portal", "confident": "confident", "wikidata": "wikidata",
           "dblp": "dblp", "gnd": "gnd"}
BATCH_NAMES = 300
BATCH_ITEMS = 2000

GAZETTEER = {   # simple queries: QLever times out on OPTIONAL with a language filter
    "countries": """CONSTRUCT { ?c wdt:P297 ?iso } WHERE { ?c wdt:P297 ?iso }""",
    "country-labels": """CONSTRUCT { ?c rdfs:label ?l } WHERE { ?c wdt:P297 ?iso ; rdfs:label ?l .
  FILTER(LANG(?l) IN (%s)) }""",
    "country-aliases": """CONSTRUCT { ?c skos:altLabel ?l } WHERE { ?c wdt:P297 ?iso ; skos:altLabel ?l .
  FILTER(LANG(?l) IN (%s)) }""",
    "subdivisions": """CONSTRUCT { ?c wdt:P300 ?code ; wdt:P17 ?country } WHERE { ?c wdt:P300 ?code ; wdt:P17 ?country }""",
    "subdivision-labels": """CONSTRUCT { ?c rdfs:label ?l } WHERE { ?c wdt:P300 ?code ; rdfs:label ?l .
  FILTER(LANG(?l) IN (%s)) }""",
    "subdivision-aliases": """CONSTRUCT { ?c skos:altLabel ?l } WHERE { ?c wdt:P300 ?code ; skos:altLabel ?l .
  FILTER(LANG(?l) IN (%s)) }""",
}
BY_NAME = """SELECT DISTINCT ?name ?i WHERE { VALUES ?name { %s }
  ?i %s ?name ; wdt:P625 ?g ; wdt:P17 ?c . }"""
FACTS = """SELECT ?i (MAX(?n) AS ?sitelinks) (MAX(?s) AS ?settlement) WHERE { VALUES ?i { %s }
  OPTIONAL { ?i wikibase:sitelinks ?n } OPTIONAL { ?i wdt:P31/wdt:P279* wd:Q486972 . BIND(1 AS ?s) } } GROUP BY ?i"""
STATEMENTS = """CONSTRUCT { ?i ?p ?o } WHERE { VALUES ?i { %s }
  VALUES ?p { wdt:P17 wdt:P625 wdt:P31 wdt:P131 wdt:P297 wdt:P300 wdt:P1082 } ?i ?p ?o }"""
LABELS = """CONSTRUCT { ?i rdfs:label ?l } WHERE { VALUES ?i { %s } ?i rdfs:label ?l . FILTER(LANG(?l) IN (%s)) }"""


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def query(q, accept):
    body = urllib.parse.urlencode({"query": PREFIXES + q}).encode("utf-8")
    for attempt in range(6):
        try:
            req = request(ENDPOINT, method="POST", data=body, headers={
                "Accept": accept, "Content-Type": "application/x-www-form-urlencoded"})
            with urllib.request.urlopen(req, timeout=600) as r:
                return r.read()
        except urllib.error.HTTPError as e:
            msg = e.read()[:300].decode("utf-8", "replace")
            if (e.code == 429 or e.code >= 500) and attempt < 5:   # QLever answers 429 also when a query timed out
                print(f"  retry {attempt + 1} after HTTP {e.code}: {msg[:120]}", flush=True)
                time.sleep(15 * (attempt + 1))
                continue
            raise RuntimeError(f"HTTP {e.code}: {msg}") from None
    raise RuntimeError("no answer")


def lit(s, lang):
    return json.dumps(s, ensure_ascii=False) + "@" + lang


def tsv_rows(body):
    lines = body.decode("utf-8").splitlines()
    return [line.split("\t") for line in lines[1:] if line]


def unbracket(t):
    return t[1:-1] if t.startswith("<") else t


def unlit(t):
    """The string of a TSV literal "Bled"@en."""
    if t.startswith('"'):
        return json.loads(t[:t.rindex('"') + 1])
    return t


def stable_triples():
    cfg, cat = config.load(), catalog.Catalog()
    files, versions = {}, {}
    for name, slug in SOURCES.items():
        v = cat.get(slug).stable
        folder = cfg.require("store") / slug / v
        files[name] = sorted(p for p in folder.glob(f"{slug}.ttl.gz"))
        versions[slug] = v
    return (lambda name: (t for p in files[name] for t in read_triples(p))), versions


def gazetteer(nt_files):
    """places.Gazetteer from the country and subdivision files of a harvest."""
    countries, subdivisions = {}, {}
    names = {}
    for path in nt_files:
        for s, p, o in read_triples(path):
            s = str(s)
            if p == places.W + "P297":
                countries[s] = o.value
            elif p == places.W + "P300":
                subdivisions.setdefault(s, [None, None])[0] = o.value
            elif p == places.W + "P17":
                subdivisions.setdefault(s, [None, None])[1] = str(o)
            elif p.endswith("#label") or p.endswith("#altLabel"):
                names.setdefault(s, set()).add(o.value)
    iso = {item: code for item, code in countries.items()}
    c = {item: (code, sorted(names.get(item, ()))) for item, code in countries.items()}
    sd = {item: (code, iso.get(country), sorted(names.get(item, ()))) for item, (code, country) in subdivisions.items()
          if code and country in iso}
    return places.Gazetteer(c, sd)


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    stats = json.loads(get(ENDPOINT + "?cmd=stats"))
    triples, versions = stable_triples()
    report = {"endpoint": ENDPOINT, "index": stats.get("name-index"), "started": now(), "datasets": versions,
              "queries": {}}
    langs = ", ".join(f'"{x}"' for x in LANGUAGES)
    for name, q in GAZETTEER.items():
        q = q % langs if "%s" in q else q
        (out / f"{name}.rq").write_text(PREFIXES + q + "\n", encoding="utf-8")
        path = out / f"{name}.nt"
        if not path.exists():
            body = query(q, "application/n-triples")
            path.write_bytes(body)
            report["queries"][name] = {"time": now(), "lines": body.count(b"\n")}
            print(name, report["queries"][name], flush=True)
    gaz = gazetteer([out / f"{n}.nt" for n in GAZETTEER])
    ments = places.mentions(triples, gaz, lambda source, iri: iri)
    names = sorted(places.names_to_look_up(ments))
    items = places.items_to_look_up(ments)
    print(f"{len(ments):,} records with mentions, {len(names):,} names, {len(items):,} items", flush=True)
    # 2. names
    for prop, fname in (("rdfs:label", "names-labels"), ("skos:altLabel", "names-aliases")):
        path = out / f"{fname}.tsv"
        if path.exists():
            continue
        rows = set()
        for i in range(0, len(names), BATCH_NAMES):
            batch = names[i:i + BATCH_NAMES]
            q = BY_NAME % (" ".join(lit(n, lg) for n in batch for lg in LANGUAGES), prop)
            if i == 0:
                (out / f"{fname}.rq").write_text(PREFIXES + q + "\n", encoding="utf-8")
            for r in tsv_rows(query(q, "text/tab-separated-values")):
                lt = r[0]
                lang = lt[lt.rindex("@") + 1:] if "@" in lt[lt.rindex('"'):] else ""
                rows.add((unlit(lt), lang, unbracket(r[1])))
            print(f"  {fname}: {min(i + BATCH_NAMES, len(names)):,} of {len(names):,} names, {len(rows):,} rows",
                  flush=True)
        path.write_text("name\tlanguage\titem\n" + "".join("\t".join(r) + "\n" for r in sorted(rows)),
                        encoding="utf-8")
        report["queries"][fname] = {"time": now(), "rows": len(rows)}
    for fname in ("names-labels", "names-aliases"):
        for line in (out / f"{fname}.tsv").read_text(encoding="utf-8").splitlines()[1:]:
            items.add(line.split("\t")[2])
    # 3. facts and statements
    items = sorted(items)
    path = out / "candidates.tsv"
    if not path.exists():
        rows = []
        for i in range(0, len(items), BATCH_ITEMS):
            q = FACTS % " ".join(f"<{x}>" for x in items[i:i + BATCH_ITEMS])
            if i == 0:
                (out / "candidates.rq").write_text(PREFIXES + q + "\n", encoding="utf-8")
            for r in tsv_rows(query(q, "text/tab-separated-values")):
                n = unlit(r[1]) if len(r) > 1 and r[1] else "0"
                n = n.split("^^")[0].strip('"') if "^^" in n else n
                s = r[2].split("^^")[0].strip('"') if len(r) > 2 and r[2] else "0"
                rows.append((unbracket(r[0]), n or "0", s or "0"))
            print(f"  candidates: {min(i + BATCH_ITEMS, len(items)):,} of {len(items):,}", flush=True)
        path.write_text("item\tsitelinks\tsettlement\n" + "".join("\t".join(r) + "\n" for r in sorted(rows)),
                        encoding="utf-8")
        report["queries"]["candidates"] = {"time": now(), "rows": len(rows)}
    path = out / "statements.nt"
    if not path.exists():
        parts = []
        for i in range(0, len(items), BATCH_ITEMS):
            vals = " ".join(f"<{x}>" for x in items[i:i + BATCH_ITEMS])
            q1, q2 = STATEMENTS % vals, LABELS % (vals, LABEL_LANGUAGES)
            if i == 0:
                (out / "statements.rq").write_text(PREFIXES + q1 + "\n", encoding="utf-8")
                (out / "labels.rq").write_text(PREFIXES + q2 + "\n", encoding="utf-8")
            parts += [query(q1, "application/n-triples"), query(q2, "application/n-triples")]
            print(f"  statements: {min(i + BATCH_ITEMS, len(items)):,} of {len(items):,}", flush=True)
        lines = sorted({line for b in parts for line in b.decode("utf-8").splitlines() if line.strip()})
        path.write_text("\n".join(lines) + "\n", encoding="utf-8")
        report["queries"]["statements"] = {"time": now(), "lines": len(lines)}
    report["finished"] = now()
    report["counts"] = {"records with mentions": len(ments), "names": len(names), "items": len(items)}
    (out / "harvest.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
