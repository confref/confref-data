# 0022 Feedback and corrections

Status: accepted · Date: 2026-11-09

## Context

confref takes its records from other sources and links them into series and events ([0013](0013-series-and-events.md),
[0017](0017-joint-and-colocated-events.md)). Errors are of two sorts: a wrong or missing fact in a record of a source,
and errors of confref's own linking and clustering. Only the second can be fixed in confref without the first coming
back with the next harvest.

## Decision

- **Feedback goes to the public issue tracker of confref-data** on GitHub, through the issue form
  `.github/ISSUE_TEMPLATE/feedback.yml` (label `feedback`), which the Feedback button of labs.confref.org fills in
  (platform decision 0008). Feedback of any kind is welcome there; it is most useful for errors of the linking and
  clustering: records linked wrongly, series or events joined or split wrongly.
- **Errors in records of a source are best also corrected at the source,** so that they are right there too; the
  correction reaches confref with the next harvest. www.confref.org/feedback/ lists the ways to report to each
  source: ConfIDent (ANNOUNCE, an account for editing), Wikidata (open editing), dblp (its FAQ on corrections), the
  GND (the GND office of the German National Library). The sources that are no longer kept (Springer LOD, the
  confref portal, the TU Wien programme committees) are corrected in confref.
- **confref creates no series or events of its own.** A missing conference is added to ConfIDent
  (<https://www.confident-conference.org/index.php/ANNOUNCE>, [0011](0011-confident.md)), which offers this as a
  service, and reaches confref from there.
- Fixes in confref follow the shared rules: new versions of generators or linksets, correction datasets, never edits
  of published files.

## Consequences

www.confref.org has a page Feedback (`/feedback/`), linked from the footer; the issue form links ConfIDent and that page
as contact links.
