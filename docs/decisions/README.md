# Decisions

One file per decision, numbered in order (format of the shared decisions in kg-commons; those are cited as `kg-commons NNNN`). A decision is changed by a new record that
supersedes the old one (the old one stays, with `Status: superseded by NNNN`). Each record: status, date, context,
decision, consequences. Short is better than complete.

| No. | Decision | Status | Date |
|---|---|---|---|
| [0001](0001-what-confref-is.md) | What confref is: open identifiers for conference series and events, joining the open sources; scope; GND linked, not imported | accepted | 2026-11-08 |
| [0002](0002-iris-and-hosts.md) | IRIs on `id.confref.org`; website `confref.org`; showcase VM `labs.confref.org` | accepted | 2026-11-08 |
| [0003](0003-repository-and-framework.md) | confref-data with the shared framework; decisions and deviations documented in kg-commons | accepted | 2026-11-08 |
| [0004](0004-shared-conventions.md) | The shared conventions of kg-commons apply (list) | accepted | 2026-11-08 |
| [0005](0005-identifiers.md) | Identifiers: opaque, base32, check character, one counter, minted only by `ids` | accepted | 2026-11-08 |
| [0006](0006-licences.md) | CC0 by default; a licence per dataset | accepted | 2026-11-08 |
| [0007](0007-sparql-and-hosting.md) | Fuseki; local development first, two VMs later | accepted | 2026-11-08 |
| [0008](0008-logo.md) | ~~The "cr" mark is the logo~~ (superseded by 0012) | superseded | 2026-11-08 |
| [0009](0009-repositories.md) | The GitHub organisation `confref` | accepted | 2026-11-08 |
| [0010](0010-legacy-data.md) | The legacy data as datasets true to their source; both 2018 IRI sets; `tuwien-pc` for reference only | accepted | 2026-11-08 |
| [0011](0011-confident.md) | ConfIDent as a dataset true to its source; needs regular updates to stay in sync | accepted | 2026-11-08 |
| [0012](0012-logo-of-the-portal.md) | The logo is the "cr" mark of portal.confref.org, redrawn as SVG | accepted | 2026-11-08 |
| [0013](0013-series-and-events.md) | Series and events: the model (series, events, proceedings; in series and held at, both many-to-many) | accepted | 2026-11-08 |
| [0014](0014-landing-pages-iris-ontology.md) | Landing pages; the IRI scheme and the ontology are published | accepted | 2026-11-08 |
| [0015](0015-site-and-dumps-on-bart.md) | The website (`www.confref.org`, `confref.org` redirects) and the dumps (`archive.confref.org`) on bart until the VMs exist | accepted | 2026-11-08 |
| [0016](0016-edition-status-mode-type.md) | Facts of an event: edition number (per series), status and attendance mode (schema.org), type (AEON classes as values) | accepted | 2026-11-08 |
| [0017](0017-joint-and-colocated-events.md) | Joint and co-located events: one event in several series, events held at a larger event, or separate events joint or co-located; the way of the source is kept | accepted | 2026-11-08 |
| [0018](0018-places.md) | Places: Wikidata items (`ls-places`, `wikidata-places`), matched by name where a source has only names | accepted | 2026-11-09 |
| [0019](0019-fields-and-disciplines.md) | Academic fields (OECD FOS 2007, `oecd-fos`) and disciplines (Wikidata items), linked in `ls-fields` | accepted | 2026-11-09 |
| [0020](0020-ratings.md) | Ratings: a kind of dataset of their own (`rating`), one dataset per source; `rating-systems` | accepted | 2026-11-09 |
| [0021](0021-governance-of-the-identifiers.md) | Governance of the identifiers: kept by the generator of `ids` alone; every version of `ids` holds their full information | accepted | 2026-11-09 |
| [0022](0022-feedback-and-corrections.md) | Feedback: any feedback as issues on confref-data; errors of sources best also reported there (ConfIDent, Wikidata, dblp, GND); new conferences via ConfIDent | accepted | 2026-11-09 |
| [0023](0023-internal-datasets.md) | Internal datasets (`internal`, internal store; not in the index, the sites or the platform); committee memberships as the first, only aggregates published | accepted | 2026-11-09 |
