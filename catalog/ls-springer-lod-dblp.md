+++
slug = "ls-springer-lod-dblp"
title = "Springer series linked to dblp, judged one by one"
author = "Kai Eckert"
example = "http://lod.springer.com/data/confseries/RelMiCS"
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
+++

The conference series of the Springer LOD data (`springer-lod`) linked to the dblp venues that Springer gave as their
dblp ids, where rules and an LLM judged the link correct (kg-commons 0037). Measured on a sample, the dblp ids of
Springer are below the quality threshold (94.5%): some name the venue of the host conference instead of a workshop
series, some a different series with the same acronym, and 387 keys of 2018 no longer exist in dblp. This linkset
keeps the links judged correct, one by one, from the evidence of both sides (the Springer conferences of the series,
the titles and proceedings of the dblp venue). The judgements were made by an LLM and not checked by people; every
link's outcome and reason is in the decisions file.
