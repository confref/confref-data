# 0003 confref-data with the shared framework; its decisions and our deviations are documented in kg-commons

Status: accepted · Date: 2026-11-08

## Context

confref needs a generator framework (catalogue, generators with run records, versions, `-meta`, store, inputs area,
corrections, linksets, identity cascade, entity pages). Such a framework exists and is used by another knowledge graph
project. confref should decide independently, and a later consolidation into one framework should stay possible.

## Decision

- **`confref-data` is the one repository for the generation, catalogue and decisions of confref.** SPARQL, the
  platform and showcases are not part of it.
- **The framework is a copy** (`src/cr/`, the command `cr`, the tests, the catalogue support files `vocabulary.toml`,
  `agents.toml`, `locations.toml`, `link-quality.toml` in confref versions), developed independently.
- **kg-commons documents what the projects share:** the decisions on the framework (cited as `kg-commons NNNN`), and
  per project where its copy comes from and every deviation that could hinder a consolidation (for confref:
  `projects/confref.md` there: what, why, how a consolidation resolves it). A deviation is recorded there when it is
  made. Changes that the other projects could take over unchanged (e.g. the project configuration) are offered back.
- **Citations:** the framework code and our documents cite the shared decisions as `kg-commons NNNN`; a number
  without prefix is a decision of this repository.

## Consequences

The confref repositories refer to kg-commons only. The origin of the copy and the diff against it are documented in
kg-commons.
