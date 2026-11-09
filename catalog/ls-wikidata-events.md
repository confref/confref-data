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
commit = "60b860c5d5d6759339bdb2ce1bd1a47a3a999cf4"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-wikidata-events-matches.tsv.gz"
  bytes = 461382
  sha256 = "7828cb25e97a1c0b72a39078ed506b3633142f9fabb9aa84469a524379853f92"

  [[versions.files]]
  path = "ls-wikidata-events.ttl.gz"
  bytes = 54415
  sha256 = "a08f20dd9953e9f54ae244526a6d3a978d7a0341391475e718ee7ed0c659eef7"
  triples = 6657

  [[versions.files]]
  path = "ls-wikidata-events-meta.ttl.gz"
  bytes = 2015
  sha256 = "8f779a4532ced15a3dfa18317b4e6b790fd7bbe45f211cab9be96ca3f831d22b"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T000959Z)."
+++

The events of `wikidata` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-wikidata-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
