# ls-springer-lod-dblp

The dblp ids of the Springer series, judged one by one (kg-commons 0037). See the docstring of `generate.py`.

1. `python3 generators/ls-springer-lod-dblp/evidence.py <dir>`: the rules and the evidence (`evidence.jsonl`,
   `rules.tsv`) from the stable versions of springer-lod and dblp.
2. Judging by `instruction.md`, in chunks; a second pass by `instruction-review.md` for the links where the judges
   disagreed with the sample judged before (`docs/reports/2026-11-09-link-quality.md`).
3. The verdicts (`verdicts.tsv`: series, dblp, verdict, reason, pass) with the evidence and the instructions go to
   the inputs area: `./cr add-input springer/dblp-verdicts-<date> …`.
4. `./cr generate ls-springer-lod-dblp`: the links judged correct (`cr:sameAs`) and the decisions file.
