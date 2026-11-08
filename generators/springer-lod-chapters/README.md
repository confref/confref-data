# springer-lod-chapters: generator history

The chapters of the lod.springer.com dump of 2018-06-04 (see `../springer-lod/README.md` for the history of the dump).

- springer-lod-chapters.ttl.gz: every triple of conferences.ttl whose subject is a chapter (`data/bookchapter/…`),
  true to the source (`../springer-lod/springer.py`).
- springer-lod-chapters-confref-2018.ttl.gz: for every chapter its IRI in the lod.confref.org copy of 2018.

Not loaded into the endpoint (papers, not conference data; also in Crossref). Oddities: as springer-lod
(`copyrightHolder` typed `xsd:integer`).
