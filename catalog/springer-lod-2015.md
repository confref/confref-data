+++
slug = "springer-lod-2015"
title = "Springer LOD: the first public version (2015)"
author = "Kai Eckert"
date = "2015-02-06"
example = "http://lod.springer.com/data/conference/semweb2014"
stable = "2026-11-08"
kind = "records"
method = ["converted"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
statement = "https://web.archive.org/web/20150329051841/http://lod.springer.com:80/wiki/bin/view/Linked+Open+Data/About"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/springer-lod-2015"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "c1e831f7ed41a5d0e6bc0da60db023985d99dc28"
description = "The first public version of the Springer conference LOD (2015-02-06), true to the source."

  [[versions.files]]
  path = "springer-lod-2015-ontology.ttl.gz"
  bytes = 794
  sha256 = "b8184e546d8b18f2f187d3fe47b650a83f0e7b3809cd050a8a345d1fc79cb205"
  triples = 109

  [[versions.files]]
  path = "springer-lod-2015.ttl.gz"
  bytes = 863960
  sha256 = "8b599af21e6f0f70c9e9d8c8de9d110c06e897387b0cf3b1b4df0d0c7e04c4e0"
  triples = 145024

  [[versions.files]]
  path = "springer-lod-2015-meta.ttl.gz"
  bytes = 1884
  sha256 = "745d9e38e953cc0a52d771d8594ce7855f0ebb223178397e5bef11da617eae5d"
  triples = 77

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T184630Z)."
+++

The first public version of the Springer conference LOD, made in the pilot of Springer and the University of Mannheim
(Volha Bryl, Kai Eckert) and published on 2015-03-05: conference series, conferences and proceedings volumes of LNCS,
LNBIP, CCIS, IFIP-AICT and LNICST, with the Springer LOD ontology of that time. Superseded in content by springer-lod
(2018), kept as the record of the first release.
