# 0006 CC0 by default; a licence per dataset

Status: accepted · Date: 2026-11-08

## Decision

- Datasets are separated by source, and every catalogue entry states its licence (a required
  field, kg-commons 0013).
- **CC0 is the default** and holds for everything we make ourselves (linksets, complements, corrections, `ids`).
- A dataset from a source under other terms (e.g. CC BY with attribution) is possible when its data is worth it; the
  licence and the attribution are then in its entry and its `-meta`. Data whose terms are unclear (ICORE rankings,
  WikiCFP) is not taken over, or only as links.
