+++
slug = "ls-wikidata-events"
title = "Wikidata events matched to the same events in dblp"
author = "Kai Eckert"
example = "http://www.wikidata.org/entity/Q54727677"
stable = "2026-11-09"
kind = "linkset"
method = ["rule-based"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"cr:sameAs" = ["dblp-event"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-wikidata-events"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "0cabaf81e04ca2b1e79948a7d00335d635e0857e"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-wikidata-events-matches.tsv.gz"
  bytes = 446011
  sha256 = "f0567989e273d4f7a9713dc22c86d152198326af1b19f481a9161537644be5a8"

  [[versions.files]]
  path = "ls-wikidata-events.ttl.gz"
  bytes = 52635
  sha256 = "9b664ea4087d4cc51cd8b5200a362d8840f39e2f8a43abbf690df4a455780b00"
  triples = 6446

  [[versions.files]]
  path = "ls-wikidata-events-meta.ttl.gz"
  bytes = 2015
  sha256 = "c33ec0ad21fcd386a020ac640ef77b043b00a14b347610c016d757e00130703f"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T235204Z)."
+++

The events of `wikidata` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-wikidata-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
