# Deviations from judaicalink-data (consolidation register)

The framework was copied from judaicalink-data at commit `0c5b6be` (2026-11-08, [decision 0003](decisions/0003-repository-and-framework.md)).
Every deviation that could hinder a later consolidation of both into one framework is listed here: what, why, and how
a consolidation resolves it. Deviate only for a good reason ([0004](decisions/0004-conventions-from-judaicalink.md)).

To see the code changes: `diff -r <(…judaicalink-data/src/jl after sed 's/\bjl\b/cr/g') src/cr`.

| # | Deviation | Why | Consolidation |
|---|---|---|---|
| X1 | **Project constants in `project.toml` / `src/cr/project.py`** instead of constants in the modules (`meta.py`, `identifiers.py`, `iris.py`, `agents.py`, `vocabulary.py`, `fetch.py`, `cli.py`, `catalog.py`, `dataindex.py`, `linkquality.py`, `linksets.py`, `classes.py`, `turtle.py`): base IRI, landing page, finder, User-Agent, framework name and repository, own ontology prefix and namespace; the name of our own IRIs as identifier source is the project name (`confref`; in judaicalink-data the literal `"judaicalink"`) | the same code for two projects | **offer back early:** with a `project.toml` holding JudaicaLink's values, judaicalink-data behaves as before. This is the main step towards a shared framework |
| X2 | **Our identifiers** `series/<id>`, `event/<id>`: type letter, base32, check character ([0005](decisions/0005-identifiers.md)), instead of `data/ep/<n>` | citable, typo-safe, typed | the minting is the same (highest number of the previous set + 1, `generators/ep/generate.py`); keep format/parse in one function that a shared framework takes as a parameter |
| X3 | **Two entity types with paths of their own** (series, event) instead of one `ep` space for all classes | conferences have two levels | the identity cascade and merge/split stay class-independent; the type decides only the path and the letter |
| X4 | **Package and command named `cr`** (`src/cr/`, `./cr`) instead of `jl` | the name of the project | mechanical (`sed 's/\bjl\b/cr/g'`); a shared framework would get a neutral name for both |
| X5 | **https** for our IRIs (`https://id.confref.org/`) instead of `http://data.judaicalink.org/` | current practice (DBLP uses https) | none: a value of `project.toml` (X1) |
| X6 | **Two tests made independent of the project:** `test_rdf.Writer.test_layout` (prefix order), `test_versions.AuthorityLinks.test_current` (sets the identity declarations instead of reading the real catalogue) | they depended on JudaicaLink's prefix and catalogue | offer back; both pass for either project |

## Not yet adapted (to do in phase 3)

The **domain tables** are still JudaicaLink's: the authority datasets and their sources (`authorities.SOURCE`,
`NOT_LINKING`), the authority namespaces, identity properties and sources (`identifiers.AUTHORITY_NAMESPACES`,
`SOURCES`, `IDENTITY`, `LITERAL_PROPERTIES`), the IRI forms of the sources (`iris.FORMS`, `VOCABULARIES`), the
classes (`classes.py`). confref needs DBLP, Wikidata, GND, ConfIDent, ROR, ORCID, DOI. For consolidation these tables
should move into the project configuration as well (a deviation once we change them; list it here then).
