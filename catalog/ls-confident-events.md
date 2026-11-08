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
commit = "933fbf2f445c3b7f020aa4b30cf631ba5c365f7c"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-confident-events-matches.tsv.gz"
  bytes = 500431
  sha256 = "f394e0f1876107d59231c9eabb418558e87cd6eaef3c81819699bc9528784c40"

  [[versions.files]]
  path = "ls-confident-events.ttl.gz"
  bytes = 55690
  sha256 = "ab0332557c3ac8b91cf53150b378e42340fb0718f4fb3bc74eb87c10055932f4"
  triples = 8651

  [[versions.files]]
  path = "ls-confident-events-meta.ttl.gz"
  bytes = 2028
  sha256 = "58048cc6352dfefeee15efc8164ea93b0b0bc44924412c60dd4a88172d50631c"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T234010Z)."
+++

The events of `confident` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-confident-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
