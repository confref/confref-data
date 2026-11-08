"""Shared by the Springer LOD datasets (springer-lod, springer-lod-chapters, springer-lod-2015): reading the dumps and
writing them true to the source (decision 0010).

True to the source means: every triple as Springer published it, with two changes that apply to every dataset
(judaicalink-data 0030 and docs/iri-forms.md there): Dublin Core elements become dcterms (the dataset descriptions use
dc:creator, dc:date, …), and IRIs of known sources are written in their canonical form (GND: https). Known oddities of
the source stay (see the READMEs).
"""

import codecs
import zipfile

from cr import iris
from cr.rdf import IRI, RDF_TYPE, BNode, TurtleParser

DC, DCT = "http://purl.org/dc/elements/1.1/", "http://purl.org/dc/terms/"
OWL = "http://www.w3.org/2002/07/owl#"
SPRINGER = "http://lod.springer.com/data/"
CONFREF_2018 = "http://lod.confref.org/data/"   # the IRIs of the copy on lod.confref.org (2018-08)
CLASS, PROPERTY = SPRINGER + "ontology/class/", SPRINGER + "ontology/property/"
CHAPTER = SPRINGER + "bookchapter/"


def normal(triples):
    """dc: elements as dcterms:, known IRIs in canonical form."""
    def dcterms(ts):
        for s, p, o in ts:
            yield s, (IRI(DCT + p[len(DC):]) if p.startswith(DC) else p), o
    return iris.canonical_triples(dcterms(triples))


def zip_triples(path, member, report=None):
    """The triples of a Turtle file in a zip archive, read as a stream."""
    with zipfile.ZipFile(path) as z, z.open(member) as f:
        text = codecs.getreader("utf-8")(f, errors="strict")
        yield from TurtleParser(text, member, report if report is not None else {}).triples()


def is_chapter(s):
    return not isinstance(s, BNode) and s.startswith(CHAPTER)


class Iris:
    """Collects the lod.springer.com IRIs of the triples passed through (subjects, objects, properties, classes)."""

    def __init__(self, subjects_only=False):
        self.seen = set()
        self.subjects_only = subjects_only

    def watch(self, triples):
        for t in triples:
            terms = (t[0],) if self.subjects_only else (t[0], t[1], t[2])
            for x in terms:
                if isinstance(x, str) and not isinstance(x, BNode) and x.startswith(SPRINGER):
                    self.seen.add(str(x))
            yield t

    def confref_2018(self):
        """For every IRI seen, its IRI on lod.confref.org (2018): owl:equivalentClass for the classes,
        owl:equivalentProperty for the properties, owl:sameAs for everything else. The copy of 2018 replaced every
        "springer.com" by "confref.org"; only lod.springer.com IRIs are mapped (decision 0010)."""
        for x in sorted(self.seen):
            p = (OWL + "equivalentClass" if x.startswith(CLASS) else
                 OWL + "equivalentProperty" if x.startswith(PROPERTY) else OWL + "sameAs")
            yield IRI(CONFREF_2018 + x[len(SPRINGER):]), IRI(p), IRI(x)


def count_types(triples, counter):
    for t in triples:
        if t[1] == RDF_TYPE:
            counter[str(t[2])] = counter.get(str(t[2]), 0) + 1
        yield t
