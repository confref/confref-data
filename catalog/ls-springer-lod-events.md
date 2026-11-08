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
commit = "933fbf2f445c3b7f020aa4b30cf631ba5c365f7c"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-springer-lod-events-matches.tsv.gz"
  bytes = 731292
  sha256 = "9021a84da7d74342170f570445c5e134644a1fbda2985513ce15c97d5e4fa3b6"

  [[versions.files]]
  path = "ls-springer-lod-events.ttl.gz"
  bytes = 88787
  sha256 = "fe6ecf1ceaf9f1fe10981d6b498e87d8f1cc4e5fa6da8bd0a420e6934759a63b"
  triples = 18187

  [[versions.files]]
  path = "ls-springer-lod-events-meta.ttl.gz"
  bytes = 2082
  sha256 = "d4a9a01562c08328672c5483e0f620e6a56331ca5e82aa9fada66294dc7c2bd9"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T233919Z)."
+++

The events of `springer-lod` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-springer-lod-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
