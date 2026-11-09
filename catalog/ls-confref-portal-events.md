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
commit = "60b860c5d5d6759339bdb2ce1bd1a47a3a999cf4"
description = "Made by the rules of events.py from springer-lod 2026-11-08, confref-portal 2026-11-09, confident, wikidata and dblp 2026-11-08 and ls-springer-lod-dblp 2026-11-09."

  [[versions.files]]
  path = "ls-confref-portal-events-matches.tsv.gz"
  bytes = 2144820
  sha256 = "06d23f5c23afa3cab04f6f613c5f13dd046519ecd0f65627ad6b18911f4de618"

  [[versions.files]]
  path = "ls-confref-portal-events.ttl.gz"
  bytes = 245085
  sha256 = "ea4696a61de1a033fdc04f1b8ae89c3116bac10daefa669f1872b8c59a99f019"
  triples = 42523

  [[versions.files]]
  path = "ls-confref-portal-events-meta.ttl.gz"
  bytes = 2067
  sha256 = "db8080deba5e1fa5eebde470c8c6087fa907cc6f87798e51368c8b465a149b0b"
  triples = 87

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T000904Z)."
+++

The events of `confref-portal` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-confref-portal-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
