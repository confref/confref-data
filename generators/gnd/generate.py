"""gnd: the records of the GND that our datasets name, as the DNB states them (kind authority).

Source: inputs:gnd/<date>, the records fetched from the Linked Data Service of the DNB (harvest.py), and the stable
versions of the datasets that name them (selection.SOURCES; the selection is made again here from the same versions
and must be covered by the harvest). CC0 (DNB).

1. The selection list (gnd-selection.tsv.gz, the format of judaicalink-data's authority datasets): one row per GND
   number and reason, with the current number the DNB answers with (empty if the number does not exist any more).
   - linked: a number named in one of the datasets (the detail is the dataset).
   - follows: a number a selected record names as its place or as a related conference (the detail is the property).
2. The data (gnd.ttl.gz): every current record, its statements as the DNB gives them (IRIs of known sources in
   canonical form). Left out: the description document (<record>/about: licence, dates of creation and change,
   description level, creator) and wdrs:describedby. The blank nodes of a record (the geometry of a place, a few
   variant name entities and relations) become resources data/gnd/node/<hash>, the hash of the statement that names
   them and of their own statements, so that the same node always has the same IRI.
3. Replacements: <https://d-nb.info/gnd/<old>> dcterms:isReplacedBy <https://d-nb.info/gnd/<n>> for a number the DNB
   redirects; <https://d-nb.info/gnd/<n>> owl:deprecated true for a number it does not know.
"""

import gzip
import hashlib
import io
import json
from collections import defaultdict

from cr import iris, project
from cr.generator import GeneratorError, load_shared
from cr.rdf import IRI, XSD, BNode, Literal, nt, read_triples

selection = load_shared("gnd", "selection")

INPUTS = {"harvest": "inputs:gnd/2026-11-08",
          "springer-lod": "springer-lod/2026-11-08", "dblp": "dblp/2026-11-08", "wikidata": "wikidata/2026-11-08"}
PARAMS = {}

GND = "https://d-nb.info/gnd/"
DCT, OWL = "http://purl.org/dc/terms/", "http://www.w3.org/2002/07/owl#"
DESCRIBEDBY = "http://www.w3.org/2007/05/powder-s#describedby"
NODE = project.DATA + "gnd/node/"


def skolemised(triples):
    """The triples of one record, each blank node replaced by data/gnd/node/<hash>."""
    triples = list(triples)
    about = {}
    for s, p, o in triples:
        if isinstance(s, BNode):
            about.setdefault(s, []).append((p, o))

    def content(b, seen):
        lines = []
        for p, o in about.get(b, []):
            if isinstance(o, BNode):
                o = "[" + (content(o, seen | {b}) if o not in seen else "") + "]"
            else:
                o = nt(o, canonical=True)
            lines.append(nt(p) + " " + o)
        return " ; ".join(sorted(lines))

    names = {}
    for s, p, o in triples:
        if isinstance(o, BNode) and not isinstance(s, BNode) and o not in names:
            key = "\t".join((nt(s), nt(p), content(o, frozenset())))
            names[o] = IRI(NODE + hashlib.sha256(key.encode("utf-8")).hexdigest()[:24])
    changed = True
    while changed:   # nodes named only by other nodes
        changed = False
        for s, p, o in triples:
            if isinstance(o, BNode) and s in names and o not in names:
                key = "\t".join((names[s], nt(p), content(o, frozenset())))
                names[o] = IRI(NODE + hashlib.sha256(key.encode("utf-8")).hexdigest()[:24])
                changed = True
    for s, p, o in triples:
        if isinstance(s, BNode) and s not in names or isinstance(o, BNode) and o not in names:
            raise GeneratorError(f"a blank node no record names: {s} {p} {o}")
        yield names.get(s, s) if isinstance(s, BNode) else s, p, names.get(o, o) if isinstance(o, BNode) else o


def generate(run):
    harvest = {p.name: p for p in run.inputs("harvest") if p.parent.name != "records"}
    records = {p.stem: p for p in run.inputs("harvest") if p.parent.name == "records"}
    status = json.loads(harvest["status.json"].read_bytes())
    seeds = selection.seeds({slug: run.inputs(slug) for slug in selection.SOURCES})
    missing = sorted(n for n in seeds if n not in status)
    if missing:
        raise GeneratorError(f"{len(missing)} numbers of the datasets are not in the harvest, e.g. {missing[:5]}")
    reasons = defaultdict(set)   # number -> {(reason, detail)}
    for n, slugs in seeds.items():
        for s in slugs:
            reasons[n].add(("linked", s))
    for n in sorted(seeds):
        current = status[n]
        if current:
            for s, p, o in read_triples(records[current]):
                for m in selection.followed([(s, p, o)]):
                    reasons[m].add(("follows", p.rsplit("#", 1)[-1]))
    missing = sorted(n for n in reasons if n not in status)
    if missing:
        raise GeneratorError(f"{len(missing)} followed numbers are not in the harvest, e.g. {missing[:5]}")
    run.log(f"selected: {len(reasons):,} numbers ({len(seeds):,} linked)")

    rows = ["gnd\tcurrent\treason\tdetail"]
    for n in sorted(reasons):
        for reason, detail in sorted(reasons[n]):
            rows.append(f"{n}\t{status[n] or ''}\t{reason}\t{detail}")
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    run.path("gnd-selection.tsv.gz").write_bytes(buf.getvalue())
    run.log(f"wrote gnd-selection.tsv.gz: {len(rows) - 1:,} rows")

    current = sorted({status[n] for n in reasons if status[n]})

    def data():
        for number in current:
            for s, p, o in skolemised(read_triples(records[number])):
                if s.endswith("/about") or p == DESCRIBEDBY:
                    continue
                yield s, p, o
        for n in sorted(reasons):
            if status[n] is None:
                yield IRI(GND + n), IRI(OWL + "deprecated"), Literal("true", XSD + "boolean", None)
            elif status[n] != n:
                yield IRI(GND + n), IRI(DCT + "isReplacedBy"), IRI(GND + status[n])

    run.write_turtle("gnd.ttl.gz", iris.canonical_triples(data()))
    run.log(f"records: {len(current):,}; replaced: {sum(1 for n in reasons if status[n] and status[n] != n):,}; "
            f"unknown: {sum(1 for n in reasons if status[n] is None):,}")
