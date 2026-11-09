# Open issues

- **Link quality for confref:** the `[linkquality]` tables of `domain.toml` and the evidence for record datasets as
  targets (dblp, Wikidata, ConfIDent) come with the identity declarations (phase 3, step 2).
- **Data errors found in Wikidata** (rejected by the syntax of `domain.toml`): P8926 `streams/conf/cibb` (2), a URL as
  P8926 (1), P10692 `conf/bncod` (a venue key, not an event).
- **ConfIDent:** regular updates of `confident` to stay in sync (frequency open); later a process for following
  their curation (deletions, merges) and for reporting disagreements to them (decision 0011).
- **Governance of the identifiers** (who keeps them, what happens if confref ends): a decision before publishing; asked
  for by the reviewers of the DSJ paper and of ConfIDent 2.
- **The 2015 Springer data** has IRIs in `lod.springer.com` like the 2018 dump; check overlaps when both are datasets.
- **Identifiers with two records of one source** (`ids` 2026-11-09: 274 events, 130 series): mostly joint events
  whose partner conferences the portal lists separately and dblp under one table of contents (APPROX/RANDOM 2011,
  ISPA/TrustCom 2016, SOCO-CISIS-ICEUTE 2013; allowed by decision 0017), and duplicates in the GND (FASE 2016). Some
  are wrong joins: AusAI 2013 and SGAI 2013 (both "AI 2013", portal events), the portal series NODE with JIT. To be
  reviewed; fixes as correction datasets or rules of the event linksets.
- **Umbrella events and their parts** (federated and joint conferences): the main remaining risk of the event rules
  (`docs/reports/2026-11-09-link-quality.md`).
