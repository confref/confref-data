# Link quality, 2026-11-09

The identity links declared in the catalogue (kg-commons 0032), measured on the stable versions of 2026-11-08 (for
`confref-portal`: 2026-11-09). Samples drawn with `./cr sample-links` (seed 2026, 100 links per unit, all links of a
unit up to 150), judged from the evidence of both sides (names, acronyms, dates, places, series, edition numbers,
classes) as correct, wrong or undecidable; strict about level (series, event, proceedings) and edition, lenient about
wording and renamed series. Accuracy = correct / (correct + wrong), with the 95% interval (Wilson). The samples and
verdicts are in `lokal/work/link-quality-2026-11-09/` (not published). The results are in
`catalog/link-quality.toml`.

| Dataset | Property | Target | Links | Sample | Correct | Wrong | Undecidable | Accuracy (95% interval) |
|---|---|---|--:|--:|--:|--:|--:|---|
| confident | DBLP_Series_ID | dblp-venue | 606 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| confident | Wikidata_Series_ID | wikidata | 591 | 100 | 93 | 2 | 5 | 98% (93%–99%) |
| confref-portal | dblpId | dblp-venue | 4,909 | 100 | 96 | 1 | 3 | 99% (94%–100%) |
| dblp | sameAs | wikidata | 6,406 | 100 | 80 | 0 | 20 | 100% (95%–100%) |
| dblp | sameAs | gnd | 12 | 12 | 9 | 2 | 1 | 82% (52%–95%) |
| gnd | sameAs | wikidata | 6,628 | 100 | 73 | 2 | 25 | 97% (91%–99%) |
| springer-lod | hasGNDID | gnd | 5,838 | 100 | 100 | 0 | 0 | 100% (96%–100%) |
| springer-lod | hasDBLPID | dblp-venue | 1,763 | 100 | 79 | 4 | 17 | 95% (88%–98%) |
| springer-lod-2015 | hasDBLPID | dblp-venue | 1,056 | 100 | 92 | 7 | 1 | 93% (86%–97%) |
| wikidata | P227 | gnd | 4,987 | 100 | 98 | 2 | 0 | 98% (93%–99%) |
| wikidata | P8926 | dblp-venue | 4,402 | 100 | 98 | 0 | 2 | 100% (96%–100%) |
| wikidata | P8978 | dblp-rec | 4,311 | 100 | 69 | 1 | 30 | 99% (92%–100%) |

Not judged: `confident` `Wikidata_Organization_ID` (organisers, not declared as identity). Not measurable, because
no dataset holds the targets: DOIs (dblp, Wikidata, ConfIDent), dblp event IDs (Wikidata P10692), WikiCFP IDs.
These join without a measurement (kg-commons 0032).

## Below the threshold (linked, but they join nothing)

- **springer-lod → dblp (95%, lower bound 88%)** and **springer-lod-2015 → dblp (93%)**. Two patterns:
  - a workshop series of Springer linked to the dblp venue of its host conference (NFMCP → ECML, MICCAI and ECCV
    workshops → MICCAI, ECCV, Data Privacy Management → ESORICS, OAMAS → ATAL, IDGD → HCI International);
  - different series that share an acronym or key (Multimedia Communications, Services and Security → Multi-Carrier
    Systems & Solutions, both MCSS; Analogical and Inductive Inference → Adaptive Lifelong Learning, key "all").

  In the samples, every workshop-to-host link has a dblp key that differs from the Springer series key; where both
  keys are equal, the wrong links are acronym clashes.
- **dblp → GND (82%, 12 links; not declared):** a proceedings volume linked to a GND event; CPS-IoT Week linked to
  the CyPhy workshop series.

## Findings

- **16 of the 100 sampled springer-lod links name dblp keys that dblp no longer has** (e.g. `conf/canadianai`,
  `conf/pro-ve`, `conf/wise-ifip`; the dblp endpoint has no statement about them): outdated keys of 2018.
  springer-lod-2015 has 78 empty dblp IRIs (`http://dblp.org/db/conf/`).
- **Undecidable links come mostly from missing evidence, not from doubtful links:** Wikidata items outside our
  selection (cities, some proceedings), GND place records without labels in the sample, Wikidata proceedings whose
  label is only the recurring series title (no year or number).
- **Level errors in Wikidata and ConfIDent are rare but exist:** a ConfIDent series linked to the Wikidata item of
  one edition (SLE, INLG); a Wikidata event linked to the GND record of its umbrella event (FASE 2005 → ETAPS 2005).
- **Umbrella and catch-all streams of dblp** (the Dagstuhl publications, MICCAI) attract links of workshops and
  seminar series.
- **Verdicts based on knowledge beyond the evidence** (marked correct): ConfIDent AAMAS → `conf/atal` (dblp files
  AAMAS under ATAL), ConfIDent RBAC → SACMAT (renamed), portal Independent Component Analysis → LVA/ICA.

## Next

- springer-lod → dblp: a judged linkset (kg-commons 0037) with the correct links, or a rule (equal keys) checked on a
  sample. The Springer series are the largest legacy source of dblp keys.
- The evidence: resolve GND places and Wikidata places to names for the samples.
