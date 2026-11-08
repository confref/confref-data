"""tuwien-pc: the programme committees of 45 conferences by the Linked Data Lab of TU Wien (2015, decision 0010).

Source: inputs:tuwien/pc-2015/PC_data_1109.ttl, the last delivery (2015-11-09) for the Springer LOD pilot: 3,944
memberships (name, title, role, affiliation, country) in 45 committees, in the model of lod.springer.com
(spr:Membership, spr:belongsToCommittee, spr:belongsToConference; affiliations and countries as "disambiguated
literals" with a DBpedia IRI where one was found). It contains all committees of the earlier deliveries (2015-05-22
to 2015-09-11, in the inputs area). Written true to the source (generators/springer-lod/springer.py).

Kept for reference only: no other dataset reads it (decision 0010).
"""

from cr.generator import load_shared

springer = load_shared("springer-lod", "springer")

INPUTS = {"pc": "inputs:tuwien/pc-2015/PC_data_1109.ttl"}
PARAMS = {}


def generate(run):
    types = {}
    run.write_turtle("tuwien-pc.ttl.gz", springer.count_types(springer.normal(run.triples("pc")), types))
    for cls, n in sorted(types.items()):
        run.log(f"  {cls}: {n:,}")
