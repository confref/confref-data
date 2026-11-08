+++
slug = "ls-springer-lod-dblp"
title = "Springer series linked to dblp, judged one by one"
author = "Kai Eckert"
example = "http://lod.springer.com/data/confseries/RelMiCS"
stable = "2026-11-09"
kind = "linkset"
method = ["rule-based", "llm-judged"]
inputs = ["springer-lod", "dblp"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"cr:sameAs" = ["dblp-venue"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-springer-lod-dblp"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "3ea4797e12041c6b2a02bef831b026debda6878c"
description = "Made from springer-lod 2026-11-08, dblp 2026-11-08 and the judgements of 2026-11-09 (kg-commons 0037): 1,311 of 1,763 dblp ids linked."

  [[versions.files]]
  path = "ls-springer-lod-dblp-decisions.tsv.gz"
  bytes = 15110
  sha256 = "759e60946661de3d53d74788be3e3f4891a437fccc428c75a670bb769fc88df2"

  [[versions.files]]
  path = "ls-springer-lod-dblp.ttl.gz"
  bytes = 8436
  sha256 = "c9e70bbffd4ab3a5010c50b94ae9a0c08920e674e03e34c2f0372eb892f65141"
  triples = 1311

  [[versions.files]]
  path = "ls-springer-lod-dblp-meta.ttl.gz"
  bytes = 2254
  sha256 = "6cdf74b1c71195e13b5dad7b8e4c34d0a653c9b86d6e866dfa524ee339a3b101"
  triples = 77

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T233302Z)."
+++

The conference series of the Springer LOD data (`springer-lod`) linked to the dblp venues that Springer gave as their
dblp ids, where rules and an LLM judged the link correct (kg-commons 0037). Measured on a sample, the dblp ids of
Springer are below the quality threshold (94.5%): some name the venue of the host conference instead of a workshop
series, some a different series with the same acronym, and 387 keys of 2018 no longer exist in dblp. This linkset
keeps the links judged correct, one by one, from the evidence of both sides (the Springer conferences of the series,
the titles and proceedings of the dblp venue). The judgements were made by an LLM and not checked by people; every
link's outcome and reason is in the decisions file.
