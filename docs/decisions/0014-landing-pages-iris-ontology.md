# 0014 Landing pages; the IRI scheme and the ontology are published

Status: accepted · Date: 2026-11-08

## Context

The framework calls the pages of its entities entity pages (kg-commons 0022). confref's entities are series and
events, and their identifiers are meant to be cited like other persistent identifiers. Users of our IRIs need to know
the scheme ([0002](0002-iris-and-hosts.md)) and our terms.

## Decision

- **Landing pages:** the page an identifier resolves to is its landing page, the term used for DOIs at Crossref and
  DataCite. `https://id.confref.org/series/<id>` and `…/event/<id>` resolve to the landing page (HTML) or to the
  data (RDF), by content negotiation on the platform. They are made from the identifier set `ids`; inside the
  framework the concept stays "entity pages".
- **The IRI scheme is public:** a section of the Identifiers page on confref.org lists the paths of 0002. The first
  path segment below `https://id.confref.org/` is reserved: `series`, `event`, `data`, `datasets`, `dumps`,
  `ontology`. Datasets are not top-level paths: a dataset is `datasets/<slug>`, its files `dumps/<slug>/…`, the
  records it coins `data/<namespace>/…` (the namespace usually its slug). A new top-level path needs a decision.
- **The ontology** is the repository `confref-ontology`: one Markdown document with the terms as Turtle blocks, from
  which the Turtle file is generated. It describes the common layer of the data: our own terms (prefix `cr:`,
  `https://id.confref.org/ontology/`) where nothing fits, and the terms of other vocabularies that `ids` and the
  linksets use, labelled with `cr:label` and `cr:comment`. Published on confref.org (`/ontology/`); the namespace
  `https://id.confref.org/ontology/` resolves there for HTML and to the Turtle file for RDF.

## Consequences

The site gets an IRI section and an ontology page; the platform redirects `id.confref.org/ontology/`. The terms of
the model ([0013](0013-series-and-events.md)) and of the identity lifecycle (`cr:sameAs`, `cr:mergedInto`,
`cr:splitInto`, `cr:retiredDate`, used by the framework) are the first in the ontology.
