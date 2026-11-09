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
commit = "60b860c5d5d6759339bdb2ce1bd1a47a3a999cf4"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-confident-events-matches.tsv.gz"
  bytes = 518585
  sha256 = "99c16d8baa332e0eec260168f395bf88af5419303bcd5088d1c736d3ba6fe9e4"

  [[versions.files]]
  path = "ls-confident-events.ttl.gz"
  bytes = 57652
  sha256 = "fab0ed1d4cf612422fa5c04c8316b55b34d0894830af9c94e0639e64fd3b4bd8"
  triples = 8941

  [[versions.files]]
  path = "ls-confident-events-meta.ttl.gz"
  bytes = 2023
  sha256 = "b75de26fc32f919a0ea37ebfeaf6c19fb33103f320515e19ad016a86d7edaef4"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T000932Z)."
+++

The events of `confident` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-confident-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
