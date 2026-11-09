+++
slug = "rating-systems"
title = "Rating systems of conferences"
author = "Kai Eckert"
example = "https://id.confref.org/data/rating-systems/core"
stable = "2026-11-09"
kind = "vocabulary"
method = ["curated"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/rating-systems"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "Six rating systems: CORE, Qualis, GII-GRIN-SCIE, CCF, Google Scholar h5-index and h5-median."

  [[versions.files]]
  path = "rating-systems.ttl.gz"
  bytes = 1028
  sha256 = "2499cff7576099f0c2efc3d35e1ecbe9e4e1613607a0e82cec04ca529b8e6299"
  triples = 50

  [[versions.files]]
  path = "rating-systems-meta.ttl.gz"
  bytes = 1448
  sha256 = "1387ea0995791c989694cb354aad4fc0712b1588f84ce99e5d8dd0b43286b0f3"
  triples = 61

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T074906Z)."
+++

The rating systems that the rating datasets refer to: the CORE ranking, Qualis, the GII-GRIN-SCIE rating, the CCF
list and the h5 indicators of Google Scholar, each with its publisher, homepage and scale.
