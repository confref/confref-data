+++
slug = "ids"
title = "confref identifiers: conference series and events"
author = "Kai Eckert"
example = "https://id.confref.org/event/e1093fb"
stable = "2026-11-09-2"
kind = "entity-pages"
method = ["deterministic"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "gnd", "ls-springer-lod-dblp",
          "ls-springer-lod-events", "ls-confref-portal-events", "ls-confident-events", "ls-wikidata-events",
          "ls-places", "wikidata-places", "ls-fields", "oecd-fos"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ids"

[[versions]]
version = "2026-11-09-2"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "Version 2: places as Wikidata items, end dates, websites, proceedings, academic fields and disciplines; the identifiers of 2026-11-09 unchanged."

  [[versions.files]]
  path = "ids-history.ttl.gz"
  bytes = 95
  sha256 = "b34916b53402effd87381a2867baf703eb4e4a7f34e433d6963e459c574e81c6"
  triples = 0

  [[versions.files]]
  path = "ids-members.tsv.gz"
  bytes = 1205141
  sha256 = "21379b9309ef6cccaf433aba6fd0f91c00957691d17f0be15e344fc4da4b4ac0"

  [[versions.files]]
  path = "ids.ttl.gz"
  bytes = 5559325
  sha256 = "5f3a038f1d8d3e62c4dd8fdaca38b78b15ced6fab905d7c1b9cbe759eaa26f8d"
  triples = 1112387

  [[versions.files]]
  path = "ids-meta.ttl.gz"
  bytes = 2295
  sha256 = "8c8918d074d3c679502c5fecfd47ec457742f4dc961c5415317dda44974a9d9c"
  triples = 119

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "1ab76e114998b8242df4d82bf72305aca77cf0dc"
description = "The first identifier set: 11,089 series and 78,280 events, numbers 32^4 to 1,137,944."

  [[versions.files]]
  path = "ids-history.ttl.gz"
  bytes = 93
  sha256 = "7f90b8fba5e79ed0a87bad541b628f11d86cf98c9ac5fb12b9b03e0068db4264"
  triples = 0

  [[versions.files]]
  path = "ids-members.tsv.gz"
  bytes = 1205141
  sha256 = "21379b9309ef6cccaf433aba6fd0f91c00957691d17f0be15e344fc4da4b4ac0"

  [[versions.files]]
  path = "ids.ttl.gz"
  bytes = 4445216
  sha256 = "08de54c393fb0860e6de50c611c73afbb523a700144dff442cd1e05165e3ce3d"
  triples = 766797

  [[versions.files]]
  path = "ids-meta.ttl.gz"
  bytes = 2184
  sha256 = "4733f69ac1866134d68aa5039b7cbe6817f959c96de441b11143f1b1f798dbf4"
  triples = 110

[[changelog]]
date = "2026-11-09"
version = "2026-11-09-2"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T075122Z)."

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T001239Z)."
+++

The confref identifiers: one identifier for every conference series (`https://id.confref.org/series/<id>`) and
every event (`https://id.confref.org/event/<id>`) that the sources know, bringing together their records about it
(`cr:sameAs`) with the main facts: names, acronyms, start and end date, place (a Wikidata item), edition number,
series, status, attendance mode, website, proceedings, academic fields and disciplines. The records are joined by the identity links that pass the quality threshold and by the linksets of confref.
Identifiers are never reused: merges, splits and retirements are recorded in `ids-history.ttl.gz`;
`ids-members.tsv.gz` lists every record of every identifier. The landing pages are made from this dataset.
