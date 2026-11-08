"""springer-lod-chapters: the 1.25 million chapters of the lod.springer.com dump of 2018-06-04 (decision 0010).

Source: inputs:springer/lod-2018 (see springer-lod): the subjects data/bookchapter/… of conferences.ttl, written true to
the source (generators/springer-lod/springer.py). The chapters are papers, not conference data: the dataset is kept
in the store and not loaded into the endpoint. springer-lod-chapters-confref-2018.ttl.gz states for every chapter its
IRI in the copy on lod.confref.org (2018-08); the books, classes and properties are mapped in springer-lod.
"""

from cr.generator import load_shared

springer = load_shared("springer-lod", "springer")

INPUTS = {"dump": "inputs:springer/lod-2018/lodspringerdump.zip"}
PARAMS = {}


def generate(run):
    seen = springer.Iris(subjects_only=True)

    def chapters():
        for t in springer.zip_triples(run.input("dump"), "conferences.ttl"):
            if springer.is_chapter(t[0]):
                yield t

    run.write_turtle("springer-lod-chapters.ttl.gz", seen.watch(springer.normal(chapters())))
    run.write_turtle("springer-lod-chapters-confref-2018.ttl.gz", seen.confref_2018())
