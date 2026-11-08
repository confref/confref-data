"""springer-lod: the conference data of lod.springer.com as of 2018-06-04, without the chapters (decision 0010).

Source: inputs:springer/lod-2018, the complete dump of the Springer LOD conference portal (conferences.ttl,
ontology.ttl), handed over by Net Wise on 2018-06-13. CC0 (the dataset description in the dump; the About page of
lod.springer.com, 2015). Everything except the chapters (subjects data/bookchapter/…, the dataset
springer-lod-chapters): conference series, conferences, books (proceedings volumes and other books), the dataset
description; the Springer LOD ontology in a file of its own.

Written true to the source (springer.py): dcterms for the Dublin Core elements, GND IRIs with https. In addition,
springer-lod-confref-2018.ttl.gz states for every lod.springer.com IRI of the dataset its IRI in the copy on
lod.confref.org (2018-08), so that both IRI sets of 2018 are the legacy base (decision 0010).
"""

from cr.generator import load_shared

springer = load_shared("springer-lod", "springer")

INPUTS = {"dump": "inputs:springer/lod-2018/lodspringerdump.zip"}
PARAMS = {}


def generate(run):
    dump = run.input("dump")
    seen = springer.Iris()
    report, types = {}, {}

    def data():
        for t in springer.zip_triples(dump, "conferences.ttl", report):
            if not springer.is_chapter(t[0]):
                yield t

    run.write_turtle("springer-lod.ttl.gz", springer.count_types(seen.watch(springer.normal(data())), types))
    for cls, n in sorted(types.items()):
        run.log(f"  {cls}: {n:,}")
    run.write_turtle("springer-lod-ontology.ttl.gz",
                     seen.watch(springer.normal(springer.zip_triples(dump, "ontology.ttl"))))
    run.write_turtle("springer-lod-confref-2018.ttl.gz", seen.confref_2018())
