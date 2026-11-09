+++
slug = "ids"
title = "confref identifiers: conference series and events"
author = "Kai Eckert"
example = "https://id.confref.org/event/e1093fb"
kind = "entity-pages"
method = ["deterministic"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "gnd", "ls-springer-lod-dblp",
          "ls-springer-lod-events", "ls-confref-portal-events", "ls-confident-events", "ls-wikidata-events"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ids"
+++

The confref identifiers: one identifier for every conference series (`https://id.confref.org/series/<id>`) and
every event (`https://id.confref.org/event/<id>`) that the sources know, bringing together their records about it
(`cr:sameAs`) with the main facts (names, acronyms, start date, place, edition number, series, status, attendance
mode). The records are joined by the identity links that pass the quality threshold and by the linksets of confref.
Identifiers are never reused: merges, splits and retirements are recorded in `ids-history.ttl.gz`;
`ids-members.tsv.gz` lists every record of every identifier. The landing pages are made from this dataset.
