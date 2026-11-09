+++
slug = "ls-springer-lod-events"
title = "Springer conferences matched to the same events in the portal, ConfIDent, Wikidata and dblp"
author = "Kai Eckert"
example = "http://lod.springer.com/data/conference/eswc2016"
stable = "2026-11-09"
kind = "linkset"
method = ["rule-based"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"cr:sameAs" = ["confref-portal", "confident", "wikidata", "dblp-event"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-springer-lod-events"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "60b860c5d5d6759339bdb2ce1bd1a47a3a999cf4"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-springer-lod-events-matches.tsv.gz"
  bytes = 748084
  sha256 = "30067dab6474f4c4a43e25349de3da74db1aebbf344edcb1a06c41dce397cf40"

  [[versions.files]]
  path = "ls-springer-lod-events.ttl.gz"
  bytes = 90096
  sha256 = "558d00e7050d1cbf06de86b3190d50f9a1f7c7a616a178adf7078beac6a65506"
  triples = 18585

  [[versions.files]]
  path = "ls-springer-lod-events-meta.ttl.gz"
  bytes = 2076
  sha256 = "ddf379b73f86a7c06a3e8b1fb9b2b503af2a145792457b19155a52d2aa1ac505"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T000838Z)."
+++

The events of `springer-lod` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-springer-lod-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
