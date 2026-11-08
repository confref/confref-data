# wikidata: generator history

The academic conferences, conference series and proceedings of Wikidata.

## Source and harvest

QLever's complete Wikidata (`https://qlever.dev/api/wikidata`; the dump of 2026-08-10 with live updates; the full
graph: the Wikidata Query Service has split scholarly articles into a graph of their own since 2025). `harvest.py
<out dir>` (about 30 seconds), then `./cr add-input wikidata/<date> <out dir>`; the selection is in the docstring of
`harvest.py`. CC0 (https://www.wikidata.org/wiki/Wikidata:Licensing).

## The generator

The harvested statements as Wikidata gives them (IRIs of known sources canonical). Only truthy statements (the
best-ranked values), no qualifiers or references; labels, aliases, descriptions only in en, de and mul.

## Known limits of the source

Wikidata's modelling of conferences is not uniform (P31 to classes or to series, series and editions mixed); the
selection takes what the classes and identifiers say, the classification is for later layers.

## History

- 2026-11-08: first harvest and version (35,271 items).
