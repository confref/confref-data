# 0020 Ratings: a kind of dataset of their own

Status: accepted · Date: 2026-11-09

## Context

Springer published ratings of conference series (CORE, Qualis, GII-GRIN-SCIE, CCF, as loaded on 2017-04-06) and the
h5 indicators of Google Scholar (2017). More rating sources may follow. A rating is an assessment by others at a
time, not a fact about a series; it changes with every edition of a ranking. Kai asked on 2026-11-09 to keep ratings
separate, as their own category of data.

## Decision

- **A new kind of dataset, `rating`** (catalogue vocabulary): ratings of series or events by a rating system, each
  with its system, value and date. The kinds of kg-commons 0013 get this value in confref (deviation in kg-commons,
  projects/confref.md).
- **Model:** a `cr:Rating` per series and system: the rated record (`cr:ratingOf`), the system (`cr:ratingSystem`, a
  concept of the vocabulary `rating-systems`), the value (`cr:ratingValue`, as the source gives it), the date
  (`dcterms:date`) and, where there is one, the page it comes from (`dcterms:source`).
- **One dataset per source and harvest** (`ratings-springer-lod`). Ratings are not copied into `ids`; landing pages
  show them through the records they rate, with system and date.
- Current CORE ranks are taken only after asking ICORE (plan of 2026-11-08).

## Consequences

The landing pages and the search show ratings as dated statements of their source. The rating systems are described
in `rating-systems`.
