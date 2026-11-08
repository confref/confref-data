# dblp: generator history

The conference part of dblp (https://dblp.org), the curated backbone of computer science conferences.

## Source

dblp publishes its data as RDF (`https://dblp.org/rdf/dblp.ttl.gz`, rebuilt daily, 2.4 GB) and through a QLever SPARQL
endpoint (`https://sparql.dblp.org/sparql`), under CC0 (`https://dblp.org/rdf/README.txt`). dblp models series
("streams", `dblp:Conference` for conference series) and publications; the proceedings volumes
(`dblp:Editorship`) stand for the editions, with their table-of-contents page (`dblp:listedOnTocPage`,
`https://dblp.org/db/conf/<stream>/<toc>`) as the edition key. Events as such (dates, places) are not modelled.

## Harvest

`harvest.py <out dir>` (about 30 seconds), then `./cr add-input dblp/<date> <out dir>`: four queries, saved with their
answers (see the docstring); the Last-Modified date of the dump at the time is recorded, since the endpoint states no
version.

## The generator

Every harvested statement as dblp gives it (IRIs of known sources canonical); the typed identifiers, blank nodes in
dblp, as `data/dblp/identifier/<hash>` (hash of record, scheme and value). Not harvested: the authorship signatures.

## History

- 2016-2019: dblp data was converted into the Springer LOD model by Maral Dadvar (HdM) from dblp's HTML pages
  (`wisslab/springer-dblp`); dblp added persistent event anchors to its pages in 2018 (mail of Marcel R. Ackermann,
  2018-03-13).
- 2026-11-08: first harvest from the SPARQL endpoint and version.
