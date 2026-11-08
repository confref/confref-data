"""ls-springer-lod-events: the events of springer-lod matched to the same events of the other sources, within linked series.

The rules are in events.py (generators/ls-springer-lod-events, shared by the ls-*-events linksets): series clusters
from the identity links that join, then per cluster and year the only event of each source, or the one event that
agrees in edition number, start date or acronym; contradicting numbers or dates block a link. This linkset holds the
links from the events of springer-lod to those of the sources after it in events.SOURCES (cr:sameAs). Writes the links and ls-springer-lod-events-matches.tsv.gz: every link
with its rule and the facts of both events.
"""

import gzip
import io
import json
from collections import Counter

from cr.generator import load_shared
from cr.rdf import IRI

events = load_shared("ls-springer-lod-events", "events")

SOURCE = "springer"
INPUTS = dict(events.INPUTS)
PARAMS = {}


def generate(run):
    uf, evs = events.read(run)
    links = [(a, b, rule) for a, b, rule in events.match(uf, evs) if a.source == SOURCE
             and not (SOURCE == "wikidata" and "has-dblp-event" in a.extra)]
    rows = ["source\ttarget\ttarget source\trule\tsource facts\ttarget facts"]
    for a, b, rule in links:
        rows.append("\t".join((a.iri, b.iri, b.source, rule, json.dumps(a.facts(), ensure_ascii=False),
                               json.dumps(b.facts(), ensure_ascii=False))))
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    run.path("ls-springer-lod-events-matches.tsv.gz").write_bytes(buf.getvalue())
    c = Counter((b.source, rule) for a, b, rule in links)
    run.note(f"{len(links):,} links of the events of springer-lod: "
             + ", ".join(f"to {t} ({r}) {n:,}" for (t, r), n in sorted(c.items())) + ".")
    run.write_turtle("ls-springer-lod-events.ttl.gz", {(IRI(a.iri), IRI(events.CR_SAME), IRI(b.iri)) for a, b, _r in links})
