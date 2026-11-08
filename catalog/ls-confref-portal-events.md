+++
slug = "ls-confref-portal-events"
title = "Events of the confref portal matched to the same events in ConfIDent, Wikidata and dblp"
author = "Kai Eckert"
example = "https://id.confref.org/data/confref-portal/event/ESWC%202016"
stable = "2026-11-09"
kind = "linkset"
method = ["rule-based"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"cr:sameAs" = ["confident", "wikidata", "dblp-event"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-confref-portal-events"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "0cabaf81e04ca2b1e79948a7d00335d635e0857e"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-confref-portal-events-matches.tsv.gz"
  bytes = 2112502
  sha256 = "13c3100f7c376615d334acdea18ac7e05f90a1201afc28e4d75eb7f6c6e8855a"

  [[versions.files]]
  path = "ls-confref-portal-events.ttl.gz"
  bytes = 241501
  sha256 = "cb0d720b6728c587ceb2abc7d94fd6bc2b16781d43a01d9c9466dfe83c0a8e0f"
  triples = 41866

  [[versions.files]]
  path = "ls-confref-portal-events-meta.ttl.gz"
  bytes = 2067
  sha256 = "759b294ef8adbed39fd649867c49e6644549c82d4b83b580368b102c6f2f0cf1"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T235110Z)."
+++

The events of `confref-portal` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-confref-portal-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
