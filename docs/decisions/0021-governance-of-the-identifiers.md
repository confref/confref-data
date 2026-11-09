# 0021 Governance of the identifiers

Status: accepted · Date: 2026-11-09

## Context

The identifiers of series and events ([0005](0005-identifiers.md)) are meant to be cited. The reviewers of the DSJ
paper and of ConfIDent 2 asked who keeps them and what happens to them if confref ends. The identifiers have been
public on id.confref.org since 2026-11-09.

## Decision

- **Kept with little effort:** the identifiers are minted and kept by the generator of the identifier set `ids`
  alone. A new version of `ids` is a run over the current versions of the sources and linksets; it keeps every
  identifier of the previous version, records merges, splits and retirements with their dates, and mints new
  identifiers deterministically. No identifier is assigned or changed by hand, so keeping them needs no curation
  beyond running the generator.
- **Independent of the platform:** every version of `ids` holds the full information of the identifiers: each
  identifier with its records in the sources (`ids-members.tsv.gz`), its history (merged, split, retired: `ids-history.ttl.gz`), its
  facts and the conflicts between the sources (`ids-conflicts.tsv.gz`). If confref becomes unavailable, the latest
  version of `ids` (CC0) is all that is needed to resolve, continue or take over the identifiers.

## Consequences

The Identifiers page of www.confref.org states both points. Copies of the versions of `ids` can be kept anywhere
under CC0; a deposit with a long-term repository is a further step.
