"""dblp: the conference part of dblp, true to the source.

Source: inputs:dblp/<date>, the answers of the dblp SPARQL endpoint (harvest.py): every statement (except those with
blank nodes) of the conference streams (dblp:Conference), of the proceedings (dblp:Editorship published in a conference
stream) and of the other streams these name (book series such as LNCS, journals), and the typed identifiers of all of
them. CC0 (dblp: "released under the CC0 1.0 Public Domain Dedication").

The statements are kept as dblp gives them, with dblp's IRIs (streams https://dblp.org/streams/…, records
https://dblp.org/rec/…, persons https://dblp.org/pid/…); IRIs of known sources in canonical form. dblp's typed
identifiers are blank nodes (datacite:hasIdentifier [ datacite:usesIdentifierScheme …; litre:hasLiteralValue … ]);
here each is a resource of its own, data/dblp/identifier/<hash>, the hash of record, scheme and value, so that the
same identifier always has the same IRI. Not harvested: the authorship signatures (dblp:hasSignature, blank nodes
with the names as printed and ORCIDs; persons come later).
"""

import hashlib

from cr import iris, project
from cr.rdf import IRI, parse_ntriples

INPUTS = {"harvest": "inputs:dblp/2026-11-08"}
PARAMS = {}

DATACITE = "http://purl.org/spar/datacite/"
LITRE = "http://purl.org/spar/literal/"
NS = project.DATA + "dblp/identifier/"
FILES = ["conference-streams.nt", "proceedings.nt", "other-streams.nt"]


def file(run, name):
    [p] = [p for p in run.inputs("harvest") if p.name == name]
    return p


def identifiers(run):
    with open(file(run, "identifiers.tsv"), encoding="utf-8") as f:
        next(f)   # header
        for line in f:
            s, scheme, value = line.rstrip("\n").split("\t")
            [(s, scheme, value)] = parse_ntriples([f"{s} {scheme} {value} .\n"], "identifiers.tsv")
            key = "\t".join((s, scheme, value.value if hasattr(value, "value") else str(value)))
            b = IRI(NS + hashlib.sha256(key.encode("utf-8")).hexdigest()[:24])
            yield s, IRI(DATACITE + "hasIdentifier"), b
            yield b, IRI(DATACITE + "usesIdentifierScheme"), scheme
            yield b, IRI(LITRE + "hasLiteralValue"), value


def generate(run):
    def data():
        for name in FILES:
            n = 0
            for t in run.triples("harvest", file=name):
                n += 1
                yield t
            run.log(f"{name}: {n:,} statements")
        yield from identifiers(run)

    run.write_turtle("dblp.ttl.gz", iris.canonical_triples(data()))
