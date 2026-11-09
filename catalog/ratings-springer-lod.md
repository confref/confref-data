+++
slug = "ratings-springer-lod"
title = "Ratings of conference series in Springer LOD (2017)"
author = "Kai Eckert"
website = "http://lod.springer.com/"
example = "https://id.confref.org/data/ratings-springer-lod/aaecc/core"
stable = "2026-11-09"
kind = "rating"
method = ["converted"]
inputs = ["springer-lod", "rating-systems"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Springer Nature (lod.springer.com)"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ratings-springer-lod"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "2,452 ratings of 742 conference series, as Springer loaded them on 2017-04-06 (rankings) and Google Scholar Metrics 2017 (h5)."

  [[versions.files]]
  path = "ratings-springer-lod.ttl.gz"
  bytes = 28307
  sha256 = "e60c12ecb03d18f02f1983a78ffe9967e5508499690baab7e71487cf916ff612"
  triples = 12952

  [[versions.files]]
  path = "ratings-springer-lod-meta.ttl.gz"
  bytes = 1741
  sha256 = "7bae59c20008538e63720e7a4534cd842579288aa5b4b1865259d99194dee484"
  triples = 67

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T074906Z)."
+++

The ratings of 742 conference series that Springer published in its linked open data: the CORE ranking, Qualis, the
GII-GRIN-SCIE rating and the CCF list as Springer loaded them on 6 April 2017, and the h5-index and h5-median of
Google Scholar of 2017. Each rating names its series, its system, its value and its date. Springer did not record
which edition of a ranking it loaded. The ratings are old; they show how a series was rated then, not now.
