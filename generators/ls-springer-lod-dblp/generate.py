"""ls-springer-lod-dblp: the dblp ids of the Springer series that rules and an LLM judged correct (kg-commons 0037).

springer-lod gives 1,763 of its conference series a dblp id (spr:hasDBLPID). Measured on a sample of 300, these links
are below the quality threshold (kg-commons 0032: 94.5%), so they join nothing. This linkset takes every one of them
and links the Springer series to the dblp venue (cr:sameAs) if
- the dblp key is a venue that dblp has (387 keys of 2018 no longer exist),
- the venue is a conference stream of dblp (not a journal or book series),
- and the verdict of the judging is "correct"; "wrong" and "undecidable" are left out. The judging
  (inputs:springer/dblp-verdicts-2026-11-09): an LLM read the evidence of both sides (made by evidence.py: the
  Springer series with up to five of its conferences, the dblp venue with its former titles and up to five of its
  proceedings) and judged each link by instruction.md, seven judges on seven chunks; a second pass judged again, by
  instruction-review.md, the links where the first pass disagreed with the sample judged before; its verdict replaces
  the first.
Writes the links and ls-springer-lod-dblp-decisions.tsv.gz: for every link of springer-lod the outcome and why (the
rule, or the verdict with its reason).
"""

import csv
import gzip
import io
from collections import Counter

from cr import identifiers, project
from cr.generator import GeneratorError
from cr.rdf import IRI, RDF_TYPE

INPUTS = {
    "springer": "springer-lod/2026-11-08",
    "dblp": "dblp/2026-11-08",
    "verdicts": "inputs:springer/dblp-verdicts-2026-11-09/verdicts.tsv",
}
PARAMS = {}

SPR = "http://lod.springer.com/data/ontology/property/"
DBLP = "https://dblp.org/rdf/schema#"
STREAMS = "https://dblp.org/streams/"
SAME = project.ONTOLOGY + "sameAs"


def generate(run):
    links = set()
    for s, p, o in run.triples("springer"):
        if p == SPR + "hasDBLPID":
            x = identifiers.identify(o, p)
            links.add((str(s), x[1] if x and x[0] == "dblp-venue" else str(o)))
    classes = {}
    for s, p, o in run.triples("dblp"):
        if p == RDF_TYPE and str(s).startswith(STREAMS):
            classes.setdefault(str(s), set()).add(str(o))
    with open(run.input("verdicts"), encoding="utf-8", newline="") as f:
        verdicts = {(r["series"], r["dblp"]): (r["verdict"], r["reason"], r["pass"])
                    for r in csv.DictReader(f, delimiter="\t")}
    out, rows, c, judged = set(), [], Counter(), set()
    for s, key in sorted(links):
        v = STREAMS + key
        if not key.startswith(("conf/", "journals/", "series/")):
            outcome, why = "left out", "not a dblp venue key"
        elif v not in classes:
            outcome, why = "left out", "venue not in dblp"
        elif DBLP + "Conference" not in classes[v]:
            outcome, why = "left out", "not a conference stream of dblp"
        elif (s, key) not in verdicts:
            raise GeneratorError(f"no verdict for {s} dblp {key}")
        else:
            judged.add((s, key))
            verdict, reason, n_pass = verdicts[(s, key)]
            outcome = "linked" if verdict == "correct" else "left out"
            why = f"judged {verdict}" + (" in the second pass" if n_pass == "2" else "") + (f": {reason}" if reason else "")
            if outcome == "linked":
                out.add((IRI(s), IRI(SAME), IRI(v)))
        c[f"{outcome}: {why.split(':')[0]}"] += 1
        rows.append((s, key, outcome, why))
    unused = set(verdicts) - judged
    if unused:
        raise GeneratorError(f"{len(unused)} verdicts for links that are not judged, e.g. {min(unused)}")
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as g, \
            io.TextIOWrapper(g, encoding="utf-8", newline="") as f:
        w = csv.writer(f, delimiter="\t", lineterminator="\n")
        w.writerow(["series", "dblp", "outcome", "why"])
        w.writerows(rows)
    run.path("ls-springer-lod-dblp-decisions.tsv.gz").write_bytes(buf.getvalue())
    run.note(f"{len(out):,} links of {len(links):,} dblp ids of springer-lod; "
             + ", ".join(f"{k} {v:,}" for k, v in sorted(c.items())) + ".")
    run.write_turtle("ls-springer-lod-dblp.ttl.gz", out)
