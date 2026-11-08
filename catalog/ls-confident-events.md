+++
slug = "ls-confident-events"
title = "ConfIDent events matched to the same events in Wikidata and dblp"
author = "Kai Eckert"
example = "https://id.confref.org/data/confident/10003"
stable = "2026-11-09"
kind = "linkset"
method = ["rule-based"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"cr:sameAs" = ["wikidata", "dblp-event"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-confident-events"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "0cabaf81e04ca2b1e79948a7d00335d635e0857e"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-confident-events-matches.tsv.gz"
  bytes = 500352
  sha256 = "785129442e48bd9b18e9cdae8b081c57c63017065b7bb1f67d9c5bde0777be5c"

  [[versions.files]]
  path = "ls-confident-events.ttl.gz"
  bytes = 55671
  sha256 = "fabea65657be599185bc53661d6d06d64a896209504553b3b037d981c033d054"
  triples = 8649

  [[versions.files]]
  path = "ls-confident-events-meta.ttl.gz"
  bytes = 2027
  sha256 = "e87b43dfed4b816141479f159f4f51f6dd00da883d5f221cf4dbaf2041307b73"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T235137Z)."
+++

The events of `confident` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-confident-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
