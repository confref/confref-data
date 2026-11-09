# 0010 The legacy data as datasets true to their source

Status: accepted · Date: 2026-11-08

## Context

The workspace archive (`old/`, registered as inputs) holds the Springer conference data of 2015, the complete
lod.springer.com dump of 2018 (CC0, stated in the data and from 2014 on in the project mails), the same dump with
lod.confref.org IRIs (2018-08), the data of portal.confref.org (API download of 2020-07-11, kept by
ConferenceCorpus), and the programme-committee data of TU Wien (2015). The 2018 dump exists nowhere else.

Compared on 2026-11-08, the lod.confref.org copy is the Springer dump with every `springer.com` replaced by
`confref.org` and with Windows line endings, nothing else: the IRIs are the only difference, except that the
replacement also turned the 59,065 links to SpringerLink (`link.springer.com/<ISBN>`) into `link.confref.org/<ISBN>`,
which never existed.

## Decision

- **`springer-lod`**: the 2018 dump without the chapters (series, conferences, proceedings volumes and other books,
  ratings, review statistics, the Springer LOD ontology), with the lod.springer.com IRIs as in the source, **and a
  file stating for every lod.springer.com IRI its lod.confref.org IRI**. So both IRI sets of 2018 are the legacy base,
  without the broken SpringerLink links of the copy.
- **The chapters** (1.25M) are not published: data on the level of papers is not confref's (Crossref has it for all
  publishers). They stay in the input `inputs:springer/lod-2018`.
- **`springer-lod-2015`**: the first public version (2015-02).
- **`confref-portal`**: the portal data of 2020, IRIs `https://id.confref.org/data/confref-portal/…`, terms in its
  namespace (`…/vocab/`), true to the API.
- **`tuwien-pc`**: the TU Wien programme committees, a dataset of its own, kept for reference: **nothing builds on it**
  (no linkset, complement or `ids` reads it). Basis: the informal OK of TU Wien (Amin Anjomshoaa, 2018-09-23).
- As everywhere (kg-commons 0030), Dublin Core elements of the sources are written as `dcterms:`, and IRIs of
  known sources in their canonical form.
- The 2018 data (both datasets) is deposited on Zenodo (CC0) when we publish, with both IRI sets.
