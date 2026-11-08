# confident: generator history

ConfIDent (https://www.confident-conference.org), the registry of academic events of TIB.

## Source

A Semantic MediaWiki (MediaWiki 1.35, SMW 4.1) with the namespaces Event Series (7100), Event (7200), Academic Field
(7300), Country (7400) and Organization (7500); organisers and deadlines of events and maintainers of series are
subobjects. CC0: page footer ("Content is available under CC0 unless otherwise noted"), Terms of Use ("Alle
eingetragenen Metadaten werden von der TIB unter der Creative Commons Licence CC0 1.0 Universal Public Domain
Dedication (CC0) veröffentlicht", revised 2023-11-02). Some event pages carry call-for-papers text copied from
WikiCFP; the harvest takes only the semantic data, no free text. ConfIDent's RDF export has malformed IRIs
(`http://https://www.confident-conference.org:443/…`) and is not used; the SPARQL endpoint of the Terms of Use was not
found (2026-11-08).

## Harvest

`harvest.py <out dir>` (one request per second; resumable), then `./cr add-input confident/<date> <out dir>`:
the Ask API with every typed property of the wiki, 250 results per request (larger pages time out on the server),
the page IDs (`list=allpages`), the log (`list=logevents`, without users and comments). About 15 minutes.

## The generator

Details in the docstring of `generate.py`: records named by the page ID (`data/confident/<page ID>`), properties
named by the SMW property (`data/confident/vocab/<Property>`; built-in properties by their label, categories as
`vocab/Category_<Category>`), values by SMW type; references to pages that do not exist as literals with the title; left out: Title_Search,
Semantic_Dependency (helpers) and Meeting_URL (online meeting links, often with passwords).

## Keeping in sync

ConfIDent is curated continuously (duplicates are deleted or moved; events are added). A new version needs a new
harvest; how often is not decided (decision 0011). Following their curation in our layers and reporting
disagreements to ConfIDent are for later (open issues).

## History

- 2026-11-08: first harvest (18:51-19:03 UTC) and version: 777,063 triples; one organisation renamed during the
  harvest (`David Tvildiani Medical UNiversity`) has no page ID in it and is left out.
