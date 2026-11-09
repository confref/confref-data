"""Harvest the Wikidata items for the academic fields and topics of our sources (the input of ls-fields).

python3 generators/ls-fields/harvest.py <out dir>

1. The names of ConfIDent's academic fields (the labels of its Academic Field pages) are looked up, in the variants of
   variants(), as English and multilingual labels and aliases (names-labels.tsv, names-aliases.tsv: the variant
   found, item).
2. Of these candidates, of the topics of the events in Wikidata (wdt:P921) and of the items in fields.ANCHORS and
   fields.PORTAL_AREAS: candidates.tsv (item, sitelinks, discipline: an instance of a subclass of one of
   fields.DISCIPLINE_CLASSES), parents.tsv (item, parent: the items it is a subclass or a part of, wdt:P279 or
   wdt:P361, one step; longer chains lead almost every topic to almost every field), labels.nt (labels in en, de,
   mul).

The queries run against QLever's complete Wikidata (https://qlever.dev/api/wikidata), by POST; harvest.json records
the endpoint, its index, the datasets read and the times.
"""

import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[1]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(HERE))
sys.path.insert(0, str(ROOT / "generators" / "ls-places"))
from cr import catalog, config  # noqa: E402
from cr.fetch import get  # noqa: E402
from cr.rdf import read_triples  # noqa: E402
import fields  # noqa: E402
import harvest as places_harvest  # noqa: E402  (the query helpers of ls-places)

ENDPOINT = places_harvest.ENDPOINT
PREFIXES = places_harvest.PREFIXES
CF = "https://id.confref.org/data/confident/vocab/"
W = "http://www.wikidata.org/prop/direct/"
WD = "http://www.wikidata.org/entity/"
BATCH = 300

BY_NAME = """SELECT DISTINCT ?name ?i WHERE { VALUES ?name { %s } ?i %s ?name . }"""
FACTS = """SELECT ?i (MAX(?n) AS ?sitelinks) (MAX(?d) AS ?discipline) WHERE { VALUES ?i { %s }
  OPTIONAL { ?i wikibase:sitelinks ?n }
  OPTIONAL { ?i wdt:P31/wdt:P279* ?c . VALUES ?c { %s } BIND(1 AS ?d) } } GROUP BY ?i"""
PARENTS = """SELECT DISTINCT ?i ?a WHERE { VALUES ?i { %s } ?i wdt:P279|wdt:P361 ?a . }"""
LABELS = """CONSTRUCT { ?i rdfs:label ?l } WHERE { VALUES ?i { %s } ?i rdfs:label ?l .
  FILTER(LANG(?l) IN ("en", "de", "mul")) }"""


def variants(name):
    """The name as written, in lower case, with a capital first letter, and with the first space as a hyphen and as
    an en dash ("Human Computer Interaction" -> "human-computer interaction", "human–computer interaction")."""
    low = name.lower()
    out = {name, low, low[:1].upper() + low[1:]}
    if " " in low:
        out |= {low.replace(" ", "-", 1), low.replace(" ", "\u2013", 1)}
    return sorted(out)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    cfg, cat = config.load(), catalog.Catalog()
    versions = {s: cat.get(s).stable for s in ("confident", "wikidata")}
    store = cfg.require("store")
    stats = json.loads(get(ENDPOINT + "?cmd=stats"))
    report = {"endpoint": ENDPOINT, "index": stats.get("name-index"), "started": now(), "datasets": versions}
    cls, label = {}, {}
    for s, p, o in read_triples(store / "confident" / versions["confident"] / "confident.ttl.gz"):
        if p.endswith("#type"):
            cls[str(s)] = str(o)
        elif p.endswith("#label"):
            label[str(s)] = o.value
    names = sorted({label[s] for s, c in cls.items() if c == CF + "Category_Academic_Field" and s in label})
    topics = set()
    for s, p, o in read_triples(store / "wikidata" / versions["wikidata"] / "wikidata.ttl.gz"):
        if p == W + "P921":
            topics.add(str(o))
    items = topics | {WD + q for q in fields.ANCHORS} | {WD + q for _f, q in fields.PORTAL_AREAS.values() if q}
    print(f"{len(names):,} field names, {len(topics):,} topics", flush=True)
    for prop, fname in (("rdfs:label", "names-labels"), ("skos:altLabel", "names-aliases")):
        rows = set()
        for i in range(0, len(names), BATCH):
            q = BY_NAME % (" ".join(places_harvest.lit(v, lg) for n in names[i:i + BATCH] for v in variants(n)
                                    for lg in ("en", "mul")), prop)
            if i == 0:
                (out / f"{fname}.rq").write_text(PREFIXES + q + "\n", encoding="utf-8")
            for r in places_harvest.tsv_rows(places_harvest.query(q, "text/tab-separated-values")):
                rows.add((places_harvest.unlit(r[0]), places_harvest.unbracket(r[1])))
        (out / f"{fname}.tsv").write_text("name\titem\n" + "".join("\t".join(r) + "\n" for r in sorted(rows)),
                                          encoding="utf-8")
        items |= {r[1] for r in rows}
        print(fname, len(rows), flush=True)
    items = sorted(i for i in items if i.startswith(WD + "Q"))
    classes = " ".join(f"wd:{c}" for c in fields.DISCIPLINE_CLASSES)
    facts, reach, labels = [], [], []
    for i in range(0, len(items), 1000):
        vals = " ".join(f"<{x}>" for x in items[i:i + 1000])
        for name, q in (("candidates", FACTS % (vals, classes)), ("parents", PARENTS % vals),
                        ("labels", LABELS % vals)):
            if i == 0:
                (out / f"{name}.rq").write_text(PREFIXES + q + "\n", encoding="utf-8")
            if name == "labels":
                labels.append(places_harvest.query(q, "application/n-triples").decode("utf-8"))
                continue
            for r in places_harvest.tsv_rows(places_harvest.query(q, "text/tab-separated-values")):
                if name == "candidates":
                    n = r[1].split("^^")[0].strip('"') if len(r) > 1 and r[1] else "0"
                    d = r[2].split("^^")[0].strip('"') if len(r) > 2 and r[2] else "0"
                    facts.append((places_harvest.unbracket(r[0]), n or "0", d or "0"))
                else:
                    reach.append((places_harvest.unbracket(r[0]), places_harvest.unbracket(r[1])))
        print(f"  {min(i + 1000, len(items)):,} of {len(items):,} items", flush=True)
    (out / "candidates.tsv").write_text("item\tsitelinks\tdiscipline\n" + "".join(
        "\t".join(r) + "\n" for r in sorted(facts)), encoding="utf-8")
    (out / "parents.tsv").write_text("item\tparent\n" + "".join("\t".join(r) + "\n" for r in sorted(set(reach))),
                                     encoding="utf-8")
    lines = sorted({x for b in labels for x in b.splitlines() if x.strip()})
    (out / "labels.nt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    report["finished"] = now()
    report["counts"] = {"field names": len(names), "topics": len(topics), "items": len(items),
                        "parent statements": len(set(reach))}
    (out / "harvest.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
