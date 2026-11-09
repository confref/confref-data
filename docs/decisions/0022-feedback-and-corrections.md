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
  (platform decision 0008). The issues are mainly about systematic errors: records linked wrongly, series or events
  joined or split wrongly, rules that go wrong in many cases.
- **Single records are corrected at their source:** data of ConfIDent can be added, edited and discussed on its site
  (<https://www.confident-conference.org/index.php/ANNOUNCE>, [0011](0011-confident.md)), Wikidata by anyone. The
  corrections reach confref with the next harvest. The form and the page Feedback of www.confref.org say so.
- Fixes in confref follow the shared rules: new versions of generators or linksets, correction datasets, never edits
  of published files.

## Consequences

www.confref.org has a page Feedback (`/feedback/`), linked from the footer; the issue form links ConfIDent and
Wikidata as contact links.
