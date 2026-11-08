# 0003 confref-data with the framework copied from judaicalink-data; deviations are recorded

Status: accepted · Date: 2026-11-08

## Context

confref needs what judaicalink-data has built (catalogue, generators with run records, versions, `-meta`, store,
inputs area, corrections, linksets, identity cascade, entity pages), but should decide independently. A later
consolidation of both into one framework should stay possible.

## Decision

- **`confref-data` is the one repository for the generation, catalogue and decisions of confref**, like
  judaicalink-data (its decision 0003). SPARQL, the platform and showcases are not part of it.
- **The framework is copied** from judaicalink-data, commit `0c5b6be` (2026-11-08): `src/jl/` → `src/cr/`, the command
  `jl` → `cr`, the tests, the catalogue support files (`vocabulary.toml`, `agents.toml`, `locations.toml`,
  `link-quality.toml`) in confref versions. From then on, both develop independently.
- **Every deviation that could hinder a consolidation is recorded** in
  [`../judaicalink-deviations.md`](../judaicalink-deviations.md) (what, why, how a consolidation resolves it), and
  mentioned when it is made. Changes that JudaicaLink could take over unchanged (e.g. the project configuration) are
  offered back.
- Decision numbers in the docstrings of `src/cr/` are those of judaicalink-data, unless they say otherwise (keeps the
  code close to the original). Our own decisions are in this folder.

## Consequences

`git diff` against judaicalink-data after `sed 's/\bjl\b/cr/g'` shows exactly what confref changed.
