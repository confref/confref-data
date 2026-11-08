# tuwien-pc: generator history

The programme committees made by the Linked Data Lab of TU Wien (Institute of Software Technology and Interactive
Systems) for the Springer LOD pilot.

## History

- 2014-11: Springer and TU Wien agree that TU Wien provides data about programme committees, hosted on
  lod.springer.com in a graph of its own, marked as provided by TU Wien.
- 2015-01 to 2015-11: student groups scrape the committees of about 50 conferences from their websites and calls for
  papers; Peb Ruswono Aryan cleans them and maps them with an extended RML processor (countries via the DBpedia
  Lookup API); deliveries 2015-05-22 (PC_data-0522), 2015-08-05, 2015-09-10, 2015-09-11, 2015-11-09 (PC_data_1109).
  Shown as a pilot on lod.springer.com (`/data/html/dataset/tuwien/conference/Arcs2015/pc`, 2015-07-10).
- 2016-01: a second source, TU Wien's conference management system ConfDriver (DEXA), reconciled with DBpedia; never
  delivered.
- 2018-09-23: Amin Anjomshoaa (TU Wien) on its use for confref: "Sure, please feel free to use the data".
- 2026-11-08: the deliveries registered as inputs:tuwien/pc-2015; this generator (decision 0010).

## The generator

tuwien-pc.ttl.gz: PC_data_1109.ttl, true to the source (`../springer-lod/springer.py`): 3,944 memberships, 7,888
disambiguated literals, 45 committees. The earlier deliveries are contained in it (all 45 committees; 30 memberships
fewer after cleaning) and stay in the inputs area.

## Use

For reference only: no other dataset reads it (decision 0010). Persons are names only (no identifiers).
