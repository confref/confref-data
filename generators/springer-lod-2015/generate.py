"""springer-lod-2015: the first public version of the Springer conference LOD (2015-02-06, decision 0010).

Source: inputs:springer/lod-2015, the N-Triples files of the Springer LOD pilot (Uni Mannheim, Volha Bryl and Kai
Eckert): conference.data.nt (series, conferences, proceedings volumes, the dataset description) and dataschema.nt (the
ontology), with their provenance files (the dataset descriptions again). CC0. Written true to the source
(generators/springer-lod/springer.py): dcterms for the Dublin Core elements. The copy in
springer_loaded_to_portal_Feb_2015.zip is identical and not read.
"""

import itertools

from cr.generator import load_shared

springer = load_shared("springer-lod", "springer")

INPUTS = {
    "data": "inputs:springer/lod-2015/conference.data.nt",
    "data_prov": "inputs:springer/lod-2015/conference.data.prov.nt",
    "schema": "inputs:springer/lod-2015/dataschema.nt",
    "schema_prov": "inputs:springer/lod-2015/dataschema.prov.nt",
}
PARAMS = {}


def generate(run):
    types = {}
    run.write_turtle("springer-lod-2015.ttl.gz", springer.count_types(
        springer.normal(itertools.chain(run.triples("data"), run.triples("data_prov"))), types))
    for cls, n in sorted(types.items()):
        run.log(f"  {cls}: {n:,}")
    run.write_turtle("springer-lod-2015-ontology.ttl.gz",
                     springer.normal(itertools.chain(run.triples("schema"), run.triples("schema_prov"))))
