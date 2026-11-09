+++
slug = "ls-fields"
title = "Academic fields and disciplines of the series and events"
author = "Kai Eckert"
example = "https://dblp.org/streams/conf/semweb"
stable = "2026-11-09"
kind = "linkset"
method = ["deterministic", "rule-based", "curated"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp", "oecd-fos"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-fields"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "OECD fields and Wikidata disciplines of the series and event records: ConfIDent (943 of 1,796 academic fields matched to Wikidata), the portal areas, the Wikidata main subjects, dblp (computer science), the Springer book series."

  [[versions.files]]
  path = "ls-fields-disciplines.tsv.gz"
  bytes = 28968
  sha256 = "e9e0343c6e2a481a18866ca3d041ee98dca1526a7b0d9b53f8a2a0146f4509de"

  [[versions.files]]
  path = "ls-fields.ttl.gz"
  bytes = 507673
  sha256 = "18227e08d9a9dd739c35e303178653920a9fb99fcb2f7db471eebd9d52af0a99"
  triples = 199638

  [[versions.files]]
  path = "ls-fields-meta.ttl.gz"
  bytes = 2434
  sha256 = "23a8583f9249917cc9f92c78b9a17d23b2deeddb41b810e839c46565d0d2dc5b"
  triples = 92

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T075022Z)."
+++

The academic fields (`cr:field`, the 42 fields of the OECD classification in `oecd-fos`) and the disciplines
(`cr:discipline`, Wikidata items) of the series and event records of the sources. ConfIDent states the field of each of
its academic fields; these are matched by name to Wikidata disciplines. The research areas of the portal are mapped by
hand. Wikidata names the main subject of many events. dblp is the bibliography of computer science, so its venues and
events are in computer and information sciences; Springer conferences get the field of the book series of their
proceedings. Each discipline gets a field as well. The file `ls-fields-disciplines.tsv.gz` lists the academic fields of
ConfIDent with the Wikidata item chosen for each.
