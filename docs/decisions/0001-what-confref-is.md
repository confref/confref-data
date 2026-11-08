# 0001 What confref is: open identifiers for conferences, joining the open sources

Status: accepted · Date: 2026-11-08

## Context

confref (2014–2022: the Springer LOD pilot, lod.confref.org, portal.confref.org) is restarted at TH Mannheim as an
open knowledge graph. The analysis of 2026-11-08 (workspace,
`ANALYSIS-2026-11-08-what-exists.md`) found no open infrastructure that gives every conference series and edition
an identifier; the sources (DBLP, Wikidata, GND, Crossref, ConfIDent) each hold a part.

## Decision

- **confref gives every academic conference series and every edition (conference, workshop, symposium) a stable,
  open identifier and joins what the open sources know about them**: proceedings, places, dates, organisers,
  subjects; later the people in their committees. Published as dumps, SPARQL and a page per entity.
- **confref coins identifiers for series and events only** ([0005](0005-identifiers.md)); proceedings keep DOI and
  ISBN, organisations ROR, places and subjects Wikidata, people ORCID, and confref links to them.
- **Scope:** scholarly events of all fields, computer science first. An event is in scope if a scholarly source names
  it (DBLP, ConfIDent, Crossref proceedings, Wikidata as an academic conference, our legacy data).
- **GND is linked, not imported.** We link our series and events to GND records, but do not take over its events
  (932,640, many not academic). Finding new events in the GND would need a dataset of its own (rule-based or another
  classification); not now.
- confref is not a call-for-papers service, makes no rankings of its own, and takes no edits from visitors (feedback
  becomes correction datasets).
- Development happens locally; nothing is published (GitHub, servers, Zenodo, Wikidata) without the OK of Kai Eckert.

## Consequences

Coverage of each source by confref is measured and published, so that "the most complete open source on
conferences" is a number, not a claim (plan, section 7.2).
