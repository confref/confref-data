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

## Outcome

- **springer-lod-2015** no longer declares identity: the series are those of springer-lod (2018), more complete.
- **springer-lod → dblp, a larger sample:** 300 links (the 100 above and 200 more, same seed): 224 correct, 13 wrong,
  63 undecidable (60 of them keys dblp no longer has): 94.5% (90.8%–96.8%), still below the threshold.
- **Every link judged** (kg-commons 0037): the linkset `ls-springer-lod-dblp` (version 2026-11-09). Rules first: 387
  of the 1,763 dblp ids name venues dblp no longer has. The other 1,376 were judged with richer evidence (up to five
  Springer conferences of the series, the former titles and up to five proceedings of the dblp venue), in seven
  chunks by one instruction; the first pass agreed with the 300-link sample on 233 of 239 links. A second pass with
  added rules (umbrella venues, venues with a main line, mixed Springer series, workshops at conferences, renames)
  judged the 6 disagreements and 18 cases the judges had flagged. Result: 1,311 linked, 62 wrong (mostly different
  series sharing an acronym or key: ICC, ICIS, ICMC, TOOLS, IDT; IFIP working-group umbrella venues; workshops linked
  to their host), 3 undecidable.

## Event linksets (phase 3, step 3)

The rule-based linksets `ls-springer-lod-events`, `ls-confref-portal-events`, `ls-confident-events` and
`ls-wikidata-events` (rules in `generators/ls-springer-lod-events/events.py`), samples drawn from their matches files
(`sample.py`, seed 2026), judged with the same criteria, strict about the edition and about a main event vs. its
workshops or satellite events. Measured on the versions before the workshop rule (below); the versions of 2026-11-09
replace them on the same day (kg-commons 0100).

| Dataset | Property | Target | Links | Sample | Correct | Wrong | Undecidable | Accuracy (95% interval) |
|---|---|---|--:|--:|--:|--:|--:|---|
| ls-confident-events | sameAs | dblp-event | 7,000 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| ls-confident-events | sameAs | wikidata | 1,651 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| ls-confref-portal-events | sameAs | dblp-event | 31,323 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| ls-confref-portal-events | sameAs | wikidata | 5,668 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| ls-confref-portal-events | sameAs | confident | 4,875 | 100 | 99 | 1 | 0 | 99% (95%–100%) |
| ls-springer-lod-events | sameAs | confref-portal | 7,680 | 100 | 100 | 0 | 0 | 100% (96%–100%) |
| ls-springer-lod-events | sameAs | dblp-event | 7,343 | 100 | 100 | 0 | 0 | 100% (96%–100%) |
| ls-springer-lod-events | sameAs | wikidata | 1,960 | 100 | 99 | 0 | 1 | 100% (96%–100%) |
| ls-springer-lod-events | sameAs | confident | 1,204 | 100 | 100 | 0 | 0 | 100% (96%–100%) |
| ls-wikidata-events | sameAs | dblp-event | 6,446 | 100 | 100 | 0 | 0 | 100% (96%–100%) |

- Check without judges: for the 171 Wikidata items that state a dblp event ID themselves (P10692), the rules find the
  same dblp event for 170; the other is the joint ESEC/FSE 2009, listed by dblp under both conferences.
- Wrong (4 of 1,000): an umbrella event and one of its parts (CISSE 2009 → SCSS 2009; IC3K 2011 → KDIR 2011); a
  workshop matched by its start date to the conference it was held with (SPLC 2008 → SOAPL 2008); the Wikidata item
  of the workshops of a conference (ICCBR 2021 → "ICCBR-WS 2021"). Undecidable (1): IC3K 2013 → a Wikidata item named
  after the proceedings of two IC3K conferences.
- Rule added: an event whose acronym marks it as the workshops of a conference ("ICCBR-WS 2021") does not match the
  conference; this removes 2 links (ICCBR 2019 and 2021). Tried and not taken: "Workshops" in a name or a dblp
  proceedings title (it removed 21 correct links of events that publish "Workshops" proceedings themselves: JSAI-isAI,
  LWDA, AICOL), and a start date only counting where the acronyms agree (it removed renamed events: HT/Hypertext,
  ISW/ISC).
- Found in ConfIDent: the event "ETAPS 2003" (number 6, Warsaw) is filed under the series CMCS (probably CMCS 2003,
  held at ETAPS); a case for reporting to ConfIDent.

## Next

- The evidence for samples: resolve GND places and Wikidata places to names.
- Umbrella events (federated and joint conferences) and their parts: links between them are the main remaining risk
  of the event rules.
