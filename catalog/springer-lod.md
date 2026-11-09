+++
slug = "springer-lod"
title = "Springer LOD: conference series, conferences and proceedings (2018)"
author = "Kai Eckert"
date = "2018-06-04"
example = "http://lod.springer.com/data/conference/ppsn2014"
stable = "2026-11-08"
kind = "records"
method = ["converted"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"spr:hasDBLPID" = ["dblp-venue"]   # on the series
"spr:hasGNDID" = ["gnd"]          # on the conferences

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
statement = "https://web.archive.org/web/20150329051841/http://lod.springer.com:80/wiki/bin/view/Linked+Open+Data/About"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/springer-lod"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "c1e831f7ed41a5d0e6bc0da60db023985d99dc28"
description = "The lod.springer.com dump of 2018-06-04 without the chapters, true to the source, with the lod.confref.org IRI of every lod.springer.com IRI."

  [[versions.files]]
  path = "springer-lod-confref-2018.ttl.gz"
  bytes = 447295
  sha256 = "8be718f470be40dd190564aab68f0b0a155652f464c5c39a052b6b31ebc134e6"
  triples = 70956

  [[versions.files]]
  path = "springer-lod-ontology.ttl.gz"
  bytes = 1958
  sha256 = "beeb0820456e8cc13b3566f5823f7ef154fe91c4c3d911bc028ea022eef1c60e"
  triples = 409

  [[versions.files]]
  path = "springer-lod.ttl.gz"
  bytes = 6368828
  sha256 = "21d369c3bca40a38ba6f7b9b303ea433481d618a49be278df3281dcea337023e"
  triples = 912826

  [[versions.files]]
  path = "springer-lod-meta.ttl.gz"
  bytes = 2345
  sha256 = "18bd992b1a669d654b71e2aa6e28004c1c3621c659472ecf641937a114b41dff"
  triples = 88

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T184623Z)."
+++

The conference data of lod.springer.com, the linked open data portal that Springer ran from 2014 with the University
of Mannheim and Net Wise, as of 2018-06-04: 1,764 conference series (all with their DBLP id, many with ratings of
CORE, GII-GRIN-SCIE, QUALIS and CCF and Google Scholar metrics), 9,327 conferences (dates, place, edition number,
5,838 with their GND id, about 690 with review statistics) and 59,684 books (the proceedings volumes with ISBN, DOI and
series, and other books). The 1.25 million chapters are not published; they stay in the input. lod.springer.com is offline; this
dump exists nowhere else.

As Springer published it (dcterms instead of the Dublin Core elements, GND IRIs with https), with the Springer LOD
ontology, and with the IRIs of the copy on lod.confref.org (2018-08) for every lod.springer.com IRI, so that both IRI
sets of 2018 are kept.
