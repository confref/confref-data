# 0011 ConfIDent as a dataset true to its source

Status: accepted · Date: 2026-11-08

## Context

ConfIDent (TIB) is a curated registry of academic events (CC0; about 20,000 events, 2,229 series, 3,424
organisations), actively maintained: curators clean up duplicates (legacy acronym pages are deleted or moved to UUID
pages) and add events.

## Decision

- **A dataset `confident`**, made from ConfIDent (SMW Ask API, page IDs from the MediaWiki API, DOIs from DataCite,
  prefix 10.25798), true to the source: it says exactly what ConfIDent says; corrections and precedence happen only in
  our own layers. Only the structured fields, no free text (call-for-papers prose may come from WikiCFP).
- **Record IRIs from the page ID:** `https://id.confref.org/data/confident/<pageid>` (the page ID survives moves, the
  title does not; their RDF IRIs are malformed). Each record states its page URL, title and DOI.
- **The dataset needs regular updates if confref is to stay in sync with ConfIDent.** How often is not decided.

## Consequences

A process for working with ConfIDent's curation (following their deletions and merges, reporting disagreements) comes
later (open issues).
