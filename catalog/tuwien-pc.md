+++
slug = "tuwien-pc"
title = "TU Wien: programme committees of 45 conferences (2015)"
author = "Kai Eckert"
date = "2015-11-09"
example = "http://lod.springer.com/data/conference/arcs2015/pc"
stable = "2026-11-08"
kind = "records"
method = ["scraped", "curated", "rule-based"]   # rule-based: the DBpedia links (lookup by name)

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Linked Data Lab, Institute of Software Technology and Interactive Systems, TU Wien (Elmar Kiesling, Peb Ruswono Aryan, Amin Anjomshoaa)"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/tuwien-pc"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "c1e831f7ed41a5d0e6bc0da60db023985d99dc28"
description = "The last delivery of TU Wien (PC_data_1109, 2015-11-09), true to the source; for reference only."

  [[versions.files]]
  path = "tuwien-pc.ttl.gz"
  bytes = 183413
  sha256 = "28c54324e98fa36eed8ff05d7428e74dc20c045602839773bef34b75c2993c0a"
  triples = 44378

  [[versions.files]]
  path = "tuwien-pc-meta.ttl.gz"
  bytes = 2094
  sha256 = "cdada4a87de42d4e3182bb86f9973c8f1da5cb3067501caed6c2f7a4c3301b7a"
  triples = 66

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T184632Z)."
+++

The programme committees of 45 conferences (2009-2015: ACISP, ARCS, CRYPTO, DEXA, ECOOP, ESWC, ISWC, MICCAI, SIGMOD
and others), 3,944 memberships with name, role, affiliation and country, made by the Linked Data Lab of TU Wien in 2015
for the Springer LOD pilot: student groups extracted the committees from the conference websites and calls for
papers, cleaned them by hand and mapped them to RDF in the model of lod.springer.com; countries and some affiliations
are linked to DBpedia. Shown as a pilot on lod.springer.com; TU Wien agreed to its use (2018).

Kept for reference only: nothing in confref builds on it (decision 0010). Persons are not identified beyond their
names.
