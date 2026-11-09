+++
slug = "confref-ontology"
title = "confref ontology"
author = "Kai Eckert"
website = "https://www.confref.org/ontology/"
example = "https://id.confref.org/ontology/Event"
stable = "2026-11-09"
kind = "ontology"
method = ["curated"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/confref-ontology"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "d7ce6eff9c1dae5168800c1ae58b4b6587ee19a8"
description = "The ontology as of confref-ontology 911907a."

  [[versions.files]]
  path = "confref-ontology.ttl.gz"
  bytes = 2796
  sha256 = "999d044fa8c4d25dbf62e5cb89ca97dfed820d0f650431c0dd60afbe1fecc207"
  triples = 157

  [[versions.files]]
  path = "confref-ontology-meta.ttl.gz"
  bytes = 1545
  sha256 = "2de39dad7cd2ceb6e6e97ebbe2400bf82c0a9414d8d60e08da2ace1f11febad0"
  triples = 62

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "First version: the terms of the identifier set ids and the linksets."
+++

The classes and properties of the confref data (decision 0014): the terms of confref (`cr:`,
`https://id.confref.org/ontology/`) where no other vocabulary has one, and how the identifier set `ids` and the
linksets use the terms of other vocabularies (schema.org, Dublin Core, SKOS, OWL). Documented on
[www.confref.org/ontology/](https://www.confref.org/ontology/); the source is the repository confref-ontology.
