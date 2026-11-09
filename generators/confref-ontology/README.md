# confref-ontology: generator history

The confref ontology (decision 0014). Its source is `confref-ontology.md` in the repository
[confref-ontology](https://github.com/confref/confref-ontology); `generate.py` there writes the Turtle file from the
code blocks of the Markdown.

## Versions

Every version is the Turtle file `confref-ontology.ttl` of confref-ontology at a commit, gzipped and imported with
`./cr import-files confref-ontology <file> --origin <the file at the commit>`; the run record names the commit.
Re-running `generate.py` on the Markdown at that commit gives the same bytes.

- 2026-11-09: confref-ontology `911907a` (series and events, facts of events, places, dates, websites, proceedings,
  fields and disciplines, ratings, identity and history).

## Reproduction

**Reproducible** from the repository confref-ontology at the commit of the run record.
