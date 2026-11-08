"""The evidence for judging the dblp ids of the Springer series (kg-commons 0037), and the rules applied first.

python3 generators/ls-springer-lod-dblp/evidence.py <out dir>

Reads the stable versions of springer-lod and dblp from the store. For every series of springer-lod with a dblp id
(spr:hasDBLPID): the rules (the venue is in dblp; it is a conference stream of dblp), then, for the links that pass,
one JSON line with the evidence of both sides: the Springer series (key, name, up to five of its conferences: name,
acronym, year, city) and the dblp venue (key, titles, former titles, up to five of its proceedings: title, year).
Writes evidence.jsonl (the links to judge, numbered i) and rules.tsv (every link: the rule outcome).
"""

import json
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from cr import catalog, config, identifiers  # noqa: E402
from cr.rdf import RDF_TYPE, Literal, read_triples  # noqa: E402

SPR, SPRC = "http://lod.springer.com/data/ontology/property/", "http://lod.springer.com/data/ontology/class/"
DBLP = "https://dblp.org/rdf/schema#"


def files(slug):
    cfg, cat = config.load(), catalog.Catalog()
    folder = cfg.require("store") / slug / cat.get(slug).stable
    return sorted(p for p in folder.glob("*.ttl.gz") if not p.name.endswith("-meta.ttl.gz") and "ontology" not in p.name
                  and "confref" not in p.name)


def val(o):
    return o.value if isinstance(o, Literal) else str(o)


def spread(items, n=5):
    """Up to n items spread over the sorted list (first, last and between)."""
    items = sorted(items)
    if len(items) <= n:
        return items
    return [items[round(k * (len(items) - 1) / (n - 1))] for k in range(n)]


def main(out):
    links, series = [], defaultdict(dict)
    conf = defaultdict(dict)
    for p in files("springer-lod"):
        for s, pr, o in read_triples(p):
            if pr == SPR + "hasDBLPID":
                x = identifiers.identify(o, pr)
                links.append((str(s), x[1] if x else None, str(o)))
            elif pr == SPR + "confSeriesName":
                series[str(s)]["name"] = val(o)
            elif pr == SPR + "hasSeries":
                conf[str(s)]["series"] = str(o)
            elif pr in (SPR + "confName", SPR + "confAcronym", SPR + "confYear", SPR + "confCity"):
                conf[str(s)][pr[len(SPR):]] = val(o)
    confs_of = defaultdict(list)
    for c in conf.values():
        if "series" in c:
            confs_of[c["series"]].append((c.get("confYear", ""), c.get("confName", ""), c.get("confAcronym", ""),
                                          c.get("confCity", "")))
    streams = {"https://dblp.org/streams/" + k: k for _s, k, _o in links if k}
    venue = defaultdict(lambda: defaultdict(list))
    procs = defaultdict(list)
    proc = defaultdict(dict)
    for p in files("dblp"):
        for s, pr, o in read_triples(p):
            s = str(s)
            if s in streams:
                if pr == RDF_TYPE:
                    venue[s]["class"].append(str(o).rsplit("#", 1)[-1])
                elif pr in (DBLP + "streamTitle", DBLP + "primaryStreamTitle", DBLP + "formerStreamTitle"):
                    venue[s][pr[len(DBLP):]].append(val(o))
            elif pr == DBLP + "publishedInStream" and str(o) in streams:
                proc[s]["stream"] = str(o)
            elif pr in (DBLP + "title", DBLP + "yearOfPublication"):
                proc[s][pr[len(DBLP):]] = val(o)
    for r in proc.values():
        if "stream" in r:
            procs[r["stream"]].append((r.get("yearOfPublication", ""), r.get("title", "")))
    out.mkdir(parents=True, exist_ok=True)
    i = 0
    with open(out / "evidence.jsonl", "w", encoding="utf-8") as ev, open(out / "rules.tsv", "w", encoding="utf-8") as ru:
        ru.write("series\tdblp\toutcome\n")
        for s, key, o in sorted(links, key=lambda x: (x[0], x[1] or "")):
            v = "https://dblp.org/streams/" + key if key else None
            if not key:
                ru.write(f"{s}\t{o}\tleft out: not a dblp venue key\n")
                continue
            if v not in venue:
                ru.write(f"{s}\t{key}\tleft out: venue not in dblp\n")
                continue
            if "Conference" not in venue[v]["class"]:
                ru.write(f"{s}\t{key}\tleft out: not a conference stream of dblp ({', '.join(venue[v]['class'])})\n")
                continue
            ru.write(f"{s}\t{key}\tjudged\n")
            ev.write(json.dumps({
                "i": i,
                "springer": {"series": s, "key": s.rsplit("/", 1)[-1], "name": series[s].get("name", ""),
                             "conferences": [" · ".join(x for x in (n, a, y, c) if x)
                                             for y, n, a, c in spread(confs_of[s])]},
                "dblp": {"venue": key, "title": venue[v]["primaryStreamTitle"] or venue[v]["streamTitle"],
                         "former titles": sorted(set(venue[v]["formerStreamTitle"])),
                         "proceedings": [f"{y} · {t}" for y, t in spread(procs[v])]},
            }, ensure_ascii=False) + "\n")
            i += 1
    print(f"{len(links):,} links, {i:,} to judge")


if __name__ == "__main__":
    main(Path(sys.argv[1]))
