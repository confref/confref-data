+++
slug = "confref-portal"
title = "confref portal: conferences of portal.confref.org (2020)"
author = "Kai Eckert"
date = "2020-07-11"
example = "https://id.confref.org/data/confref-portal/event/btw2021"
namespaces = ["confref-portal"]
stable = "2026-11-09"
kind = "records"
method = ["converted"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"portal:dblpId" = ["dblp-venue"]   # on the series

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/confref-portal"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "33bd4ffa4497321479d386b7213e250df5e9a351"
description = "The portal data of 2020-07-11 as in 2026-11-08, with the DBLP id of 145 series given by the portal as a bare key written as a literal instead of an invalid relative IRI."

  [[versions.files]]
  path = "confref-portal-vocabulary.ttl.gz"
  bytes = 840
  sha256 = "c84c707fc68b709c6de9a47602f09100c0b5d7ac43520ef72a32a0aa1cc31247"
  triples = 72

  [[versions.files]]
  path = "confref-portal.ttl.gz"
  bytes = 3292995
  sha256 = "ad0e6b9015d4888e583431bba235adcc3e4ce8fa4858f239cb53b96a6a1e36b7"
  triples = 702108

  [[versions.files]]
  path = "confref-portal-meta.ttl.gz"
  bytes = 2110
  sha256 = "88531b20958d8070b8765c40d63f5cfdc60aed89095670bb5b04bc648768b435"
  triples = 72

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "c1e831f7ed41a5d0e6bc0da60db023985d99dc28"
description = "The conferences of the portal API as downloaded on 2020-07-11, true to the API."

  [[versions.files]]
  path = "confref-portal-vocabulary.ttl.gz"
  bytes = 810
  sha256 = "ee3b548fb9aafe86cb5b9c0cccff1643315a9d2a7c887e4a66891bfb87ff118d"
  triples = 72

  [[versions.files]]
  path = "confref-portal.ttl.gz"
  bytes = 3292916
  sha256 = "5b7cf5edb3730f918f76a773ef4f5ec13c1c1d377e7530136bec3ce7e43f8183"
  triples = 702108

  [[versions.files]]
  path = "confref-portal-meta.ttl.gz"
  bytes = 2045
  sha256 = "85a0d199d94e9297d32272bfbdff27c06c4b5512c24d00cba21ba104c432211e"
  triples = 72

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "Fix: dblpId values that are bare keys are literals (relative IRIs before)."

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T184633Z)."
+++

The 37,945 conferences of 5,668 series of portal.confref.org (2019-2022), the prototype of confref built with the
Digital Science Catalyst Grant, as its API delivered them on 2020-07-11: name, acronym, place, year, dates, series
(with ISSN and DBLP id), research area and keywords. Mostly computer science, from the Springer Nature metadata API
(2002 on) and DBLP. The portal is offline; the download was kept by Wolfgang Fahl's ConferenceCorpus.

True to the API, with terms in the dataset namespace (`vocab/`). Known limits of the source: many dates are
placeholders (start and end on 1 January of the year, 6,365 events), some years are impossible (0, 19670), the
rankings were never filled.
