# 0002 IRIs on id.confref.org; the website on confref.org; the showcase VM on labs.confref.org

Status: accepted · Date: 2026-11-08

## Context

The domain confref.org is fully under our control (registered until 2027-05-18). JudaicaLink showed that a host of
its own for the IRIs pays off: data.judaicalink.org could be handed to Frankfurt without touching the website; it
also showed that paths left out of such a handover stop resolving.

## Decision

- **Every IRI we coin is on `https://id.confref.org/`** (https), with the paths of judaicalink-data decision 0018
  below it:

  | What | IRI |
  |---|---|
  | conference series, event (our identifiers, [0005](0005-identifiers.md)) | `series/<id>`, `event/<id>` |
  | a record we coin for a source without IRIs | `data/<namespace>/…` (namespace chosen per dataset, usually its slug) |
  | dataset (= graph), version, metadata graph | `datasets/<slug>`, `datasets/<slug>/<version>`, `datasets/<slug>/meta` |
  | file of a version | `dumps/<slug>/<version>/<path>` |
  | agents, catalogue vocabulary | `datasets/agents/…`, `datasets/vocabulary/…` |
  | our own terms | `ontology/` (prefix `cr:`) |

- Records of sources keep the source's IRIs where they have them (DBLP, Wikidata, GND, DOIs, lod.springer.com).
- **Hosts:** `confref.org` (with `www.` redirecting) is the stable project website: data catalogue, dumps, news.
  The showcase VM is **`labs.confref.org`**: SPARQL, the dashboard, the showcases, and the resolution of
  `id.confref.org` (HTML or RDF by content negotiation). `lod.confref.org` redirects the IRIs of 2018 to our
  identifiers; `data.confref.org` is not used (redirects to the website). `portal.confref.org` stays free: a portal
  would be planned properly later.
- The base IRI, the landing page, the finder and the User-Agent are set in `project.toml`.

## Consequences

The resolution of the identifiers can move (e.g. to a partner) by one DNS record, without the website. A subdomain
can be a CNAME; the bare domain cannot, so it carries the website.
