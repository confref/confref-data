# 0023 Internal datasets; committee memberships

Status: accepted · Date: 2026-11-09

## Context

To help people assess a conference, confref wants to use who serves on its committees and who published at its
editions (workspace notes `NOTES-2026-11-09-sources-and-assessment.md`). This is personal data. Kai's principle:
the person data itself is not published; it is used to derive relations between series and events and aggregate
factors. The process should still be as transparent as the rest of confref: the same framework, generators in the
repository, catalogue entries, run records.

## Decision

- **A catalogue entry can be internal:** the field `internal` holds the reason (`internal = "committee members:
  personal data"`). The versions of an internal dataset are kept in the **internal store** (`internal_store` in
  `local.toml`, `lokal/internal/`), never in the store, so copying the store to a dumps location cannot publish them.
  Internal datasets are not in the data index (`cr update-dataindex`), not copied to the sites (`cr sync-site`) and
  therefore not loaded on the platform. Everything else is as for every dataset: the generator, the catalogue entry,
  the run records and the -meta are in this repository, so the process is documented in public.
- **Published datasets made from internal ones** contain no person data: only aggregates per event or series and
  relations between them, and no aggregate over fewer than five persons. Such a dataset names the internal dataset as
  its input; the method is described in its generator.
- **Committee memberships** are the first internal datasets: the programme committees and organisers of events, from
  conference websites, the front matter of proceedings (CEUR-WS, Springer) and structured sources (researchr.org,
  ConfIDent where it has them). Kept: name, role, affiliation and identifiers (ORCID, dblp) as stated by the source,
  the source page and the date. Not kept: e-mail addresses, photos, anything beyond the committee lists. The TU Wien
  data (`tuwien-pc`, [0010](0010-legacy-data.md)) stays as it is.
- **Harvesting** follows the rules of all harvests: the project User-Agent, robots.txt and a polite rate, no login.
- **Legal basis:** processing of published personal data for research (GDPR Art. 6(1)(f), Art. 89). The information
  of the persons concerned (Art. 14) is given by a public description of the processing (this decision and a page on
  www.confref.org) instead of individual notices (Art. 14(5)(b)); a person can ask to be removed, and is.

## Consequences

`cr` knows the field `internal` (kg-commons register, confref X12). Before the first harvest of committees,
www.confref.org gets a privacy section on this processing (what, why, legal basis, how to object).
