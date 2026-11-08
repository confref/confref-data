+++
slug = "springer-lod-chapters"
title = "Springer LOD: chapters of the books (2018)"
author = "Kai Eckert"
date = "2018-06-04"
example = "http://lod.springer.com/data/bookchapter/978-3-319-21494-8_3"
stable = "2026-11-08"
kind = "records"
method = ["converted"]
inputs = ["springer-lod"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
statement = "https://web.archive.org/web/20150329051841/http://lod.springer.com:80/wiki/bin/view/Linked+Open+Data/About"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/springer-lod-chapters"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "c1e831f7ed41a5d0e6bc0da60db023985d99dc28"
description = "The chapters of the lod.springer.com dump of 2018-06-04, true to the source, with their lod.confref.org IRIs."

  [[versions.files]]
  path = "springer-lod-chapters-confref-2018.ttl.gz"
  bytes = 6049294
  sha256 = "14a0ef1942905a03125f3cb9f4e156452893125021af7d7e7efd2cd55e9490a4"
  triples = 1251627

  [[versions.files]]
  path = "springer-lod-chapters.ttl.gz"
  bytes = 92752721
  sha256 = "5df0bd680b289ece6e1849de4718b3425573f0682d674e416c85381eb6d9666f"
  triples = 18322692

  [[versions.files]]
  path = "springer-lod-chapters-meta.ttl.gz"
  bytes = 1985
  sha256 = "81a0b2be252d1d2a2bbbfcb22d17ed99b8dd4cd4aa07ee42d64a01d06511e264"
  triples = 74

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T184813Z)."
+++

The 1,251,627 chapters of the books in the lod.springer.com dump of 2018-06-04 (title, authors, pages, DOI, dates,
indexing in Scopus and Compendex), with their IRIs in the copy on lod.confref.org (2018-08). Papers rather than
conference data: kept as part of the legacy base, not loaded into the endpoint. The books are in springer-lod.
