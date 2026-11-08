# confref-data

Generation, organisation and description of the confref data: the generators that produce datasets, the complete
catalogue of the confref knowledge graph, and the decisions and processes behind it. confref gives conference series
and events open identifiers and joins what the open sources know about them ([decision 0001](docs/decisions/0001-what-confref-is.md)).

The framework (`src/cr/`, command `./cr`) was copied from
[judaicalink-data](https://github.com/judaicalink/judaicalink-data) (commit `0c5b6be`, 2026-11-08) and is developed
independently; deviations that matter for a later consolidation are in
[`docs/judaicalink-deviations.md`](docs/judaicalink-deviations.md). Docstrings cite judaicalink-data's decision numbers
unless they say otherwise.

| Path | What |
|---|---|
| `docs/decisions/` | decision records, one file per decision |
| `docs/process.md` | how a dataset moves from development to the catalogue and the dumps locations |
| `docs/open-issues.md` | known problems and open questions |
| `docs/judaicalink-deviations.md` | where confref deviates from judaicalink-data |
| `catalog/` | one entry per dataset (`<slug>.md`, format of judaicalink-data 0013), `agents.toml`, `vocabulary.toml`, `locations.toml`, `link-quality.toml` |
| `generators/` | one folder per dataset: its generator, README, run records |
| `project.toml` | the project: base IRI, names, User-Agent, own ontology (deviation X1) |
| `cr`, `src/cr/` | the framework and its command line: `./cr --help` |
| `tests/` | `python3 -m unittest discover -s tests` |

Local settings: `local.toml` (copy `local.example.toml`); the data lives outside the repository in `../lokal/`
(→ `~/lokal/confref/`: `store/`, `build/`, `inputs/`, `work/`). Python ≥ 3.11, standard library only.

Data files are not stored in the repository; the permanent record of what existed and how it was made is the git
history of this repository (judaicalink-data 0019).
