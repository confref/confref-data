# Open issues

- **Link quality for confref:** the `[linkquality]` tables of `domain.toml` and the evidence for record datasets as
  targets (dblp, Wikidata, ConfIDent) come with the identity declarations (phase 3, step 2).
- **Data errors found in Wikidata** (rejected by the syntax of `domain.toml`): P8926 `streams/conf/cibb` (2), a URL as
  P8926 (1), P10692 `conf/bncod` (a venue key, not an event).
- **ConfIDent:** regular updates of `confident` to stay in sync (frequency open); later a process for following
  their curation (deletions, merges) and for reporting disagreements to them (decision 0011).
- **The 2015 Springer data** has IRIs in `lod.springer.com` like the 2018 dump; check overlaps when both are datasets.
- **Identifiers with two records of one source** (`ids` 2026-11-09: 274 events, 130 series): mostly joint events
  whose partner conferences the portal lists separately and dblp under one table of contents (APPROX/RANDOM 2011,
  ISPA/TrustCom 2016, SOCO-CISIS-ICEUTE 2013; allowed by decision 0017), and duplicates in the GND (FASE 2016). Some
  are wrong joins: AusAI 2013 and SGAI 2013 (both "AI 2013", portal events), the portal series NODE with JIT. To be
  reviewed; fixes as correction datasets or rules of the event linksets.
- **Umbrella events and their parts** (federated and joint conferences): the main remaining risk of the event rules
  (`docs/reports/2026-11-09-link-quality.md`).
- **Workshop and poster volumes of dblp as events of the main series** (found on the landing pages, 2026-11-09): dblp
  lists the volumes of co-located workshops, posters and demos in the venue of the main conference (ISWC: 106
  "events"). They become events in the series of the conference (`cr:inSeries`) instead of events held at it
  (`cr:heldAt`, decision 0017), and they share its edition number ("co-located with the 19th ISWC"), so the
  agreement rule of `events.py` finds several candidates and the main volume stays unmatched: ISWC 2020 has two
  identifiers (dblp `e11s612`, the other sources `e10mxc0`). Remedies: recognise these volumes by their titles
  ("Workshops", "Posters", "co-located with") and link them with `cr:heldAt`; join events that share a proceedings
  DOI or ISBN (both identifiers of ISWC 2020 name DOI 10.1007/978-3-030-62419-4).
- **Duplicate series** seen in the search: "Semantic Web Evaluation Challenge" (2 series), "Extended Semantic Web
  Conference" (2 series). To be checked with the series clusters.
- **Names in the search:** `ids` gives one name and up to three acronyms per identifier; the names of the other
  records are not searchable on the platform. Give all names (`schema:alternateName`) in the next version.
- **Labels of dblp events** are the titles of their first proceedings volume ("The Semantic Web - ISWC 2020 - 19th
  …, Proceedings, Part I"). A shorter name could be derived from the title or taken from a matched record.
- **Place names not yet harvested:** ConfIDent's city paths ("ES/SA/Salamanca") and the region-like parts of the dblp
  titles are read since 2026-11-09 but were not in the harvest of that day; they are found at the next harvest.
