+++
slug = "springer-lod"
title = "Springer LOD: conference series, conferences and proceedings (2018)"
author = "Kai Eckert"
date = "2018-06-04"
example = "http://lod.springer.com/data/conference/ppsn2014"
kind = "records"
method = ["converted"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
statement = "https://web.archive.org/web/20150329051841/http://lod.springer.com:80/wiki/bin/view/Linked+Open+Data/About"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/springer-lod"
+++

The conference data of lod.springer.com, the linked open data portal that Springer ran from 2014 with the University
of Mannheim and Net Wise, as of 2018-06-04: 1,764 conference series (all with their DBLP id, many with ratings of
CORE, GII-GRIN-SCIE, QUALIS and CCF and Google Scholar metrics), 9,327 conferences (dates, place, edition number,
5,838 with their GND id, about 690 with review statistics) and 59,684 books (the proceedings volumes with ISBN, DOI and
series, and other books). The 1.25 million chapters are in springer-lod-chapters. lod.springer.com is offline; this
dump exists nowhere else.

As Springer published it (dcterms instead of the Dublin Core elements, GND IRIs with https), with the Springer LOD
ontology, and with the IRIs of the copy on lod.confref.org (2018-08) for every lod.springer.com IRI, so that both IRI
sets of 2018 are kept.
