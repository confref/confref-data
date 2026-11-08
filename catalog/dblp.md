+++
slug = "dblp"
title = "dblp: conference series and their proceedings"
author = "Kai Eckert"
website = "https://dblp.org/"
example = "https://dblp.org/streams/conf/esws"
namespaces = ["dblp"]
stable = "2026-11-08"
kind = "records"
method = ["converted"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"owl:sameAs" = ["wikidata", "doi"]   # the streams (Wikidata) and the proceedings (Wikidata, DOI)

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "dblp computer science bibliography, Schloss Dagstuhl – Leibniz Center for Informatics (https://dblp.org)"
statement = "https://dblp.org/rdf/README.txt"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/dblp"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "d67949a11581a3c4afef09d54dae9698deda7670"
description = "The conference part of dblp as on 2026-11-08 (dump of 2026-11-08 01:34 UTC), true to the source."

  [[versions.files]]
  path = "dblp.ttl.gz"
  bytes = 16376345
  sha256 = "b64ef95d5c2059478e226069d7f71c757db9f921089bf67774df61dc6ff6ab88"
  triples = 2072947

  [[versions.files]]
  path = "dblp-meta.ttl.gz"
  bytes = 2072
  sha256 = "f379702a7b75a4e1a31617af47538b2ea6133ace266a698c1162fb40d66da43c"
  triples = 67

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T193027Z)."
+++

The conference part of dblp, the computer science bibliography of Schloss Dagstuhl: its 7,196 conference series
("streams") with their titles, former titles, websites, Wikidata links and the relations between them (parent,
related, predecessor and successor series), the 62,560 proceedings volumes published in them (title, editors, year,
ISBN, DOI, publisher, book series and volume, the table of contents that stands for the edition, Wikidata and
OpenCitations links), and the 76 book series and journals these name. As dblp states it, from its SPARQL endpoint;
dblp's typed identifiers as resources of their own.
