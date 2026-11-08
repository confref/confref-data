+++
slug = "ls-springer-lod-events"
title = "Springer conferences matched to the same events in the portal, ConfIDent, Wikidata and dblp"
author = "Kai Eckert"
example = "http://lod.springer.com/data/conference/eswc2016"
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
+++

The events of `springer-lod` linked to the same events of other sources (`cr:sameAs`), found by rules within series that
are already linked: the series records of the sources are joined into clusters by the identity links that pass the
quality threshold (dblp venue keys, Wikidata items, and the judged linkset `ls-springer-lod-dblp`); within a cluster
and a year, an event is matched to the only event of the other source, or, where a source has several, to the one
that agrees in edition number, start date or acronym. Contradicting edition numbers or dates block a link. The file
`ls-springer-lod-events-matches.tsv.gz` lists every link with its rule and the facts of both events.
