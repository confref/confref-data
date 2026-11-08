# gnd: generator history

The GND records our datasets name (decision 0001: the GND is linked, not taken over).

## Source and harvest

The Linked Data Service of the DNB (`https://d-nb.info/gnd/<n>/about/lds`, Turtle), CC0. `harvest.py <out dir>`
reads the stable versions of springer-lod, dblp and wikidata from the store, takes every GND number they name
(`selection.py`), fetches each record, then the records these name as place or related conference (one step), and
records the redirects and unknown numbers (`status.json`); fewer than 2 requests per second, so about two hours for
the first harvest. Then `./cr add-input gnd/<date> <out dir>`.

## The generator

The selection list `gnd-selection.tsv.gz` (format of judaicalink-data's authority datasets: number, current number,
reason, detail), the records as the DNB gives them without their description documents, and the replacements
(`dcterms:isReplacedBy`, `owl:deprecated`). The selection is made again from the same versions of the datasets, and the
run fails if the harvest does not cover it. New versions of the source datasets need a new harvest (only the new
numbers are fetched if the same directory is used).

## Later

The full cascade of judaicalink-data (identity links between the authority datasets until nothing is pending) comes
with the identity layer (phase 3); then also the GND numbers ConfIDent might name.

## History

- 2017-08/09: Maral Dadvar matched 6,805 of 11,399 Springer events to the GND (the `hasGNDID` of springer-lod).
- 2026-11-08: first harvest and version.
