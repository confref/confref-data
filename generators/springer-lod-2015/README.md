# springer-lod-2015: generator history

The first public version of the Springer conference LOD (data of 2015-02-06, published 2015-03-05).

## History

- 2014-11 to 2015-02: Volha Bryl and Kai Eckert (University of Mannheim, Data and Web Science Group) convert an Excel
  export of Springer's production database (8,320 conferences, 1,306 series, sent 2015-02-06) with TSVtoRDF.java, URI
  scheme `/data/conference/…`, `/data/confseries/…`, `/data/procvolume/<ISBN>`; dumps on Dropbox, Google Drive and
  datahub.io.
- 2026-11-08: the files of the archive registered as inputs:springer/lod-2015; this generator (decision 0010).

## The generator

springer-lod-2015.ttl.gz: conference.data.nt with conference.data.prov.nt (145,024 triples: 7,129 conferences, 1,134
series, 7,868 proceedings volumes, the dataset description); springer-lod-2015-ontology.ttl.gz: dataschema.nt with
dataschema.prov.nt. True to the source (`../springer-lod/springer.py`): `dc:` elements as `dcterms:`.

## Known oddities of the source (kept)

- Dates in the form "02-Dec-09" typed `xsd:date` (ill-typed).
- One proceedings volume without ISBN: `<http://lod.springer.com/data/http://lod.springer.com/data/procvolume/>`
  (131 `hasConference` statements).
