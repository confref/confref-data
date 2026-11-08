+++
slug = "confref-portal"
title = "confref portal: conferences of portal.confref.org (2020)"
author = "Kai Eckert"
date = "2020-07-11"
example = "https://id.confref.org/data/confref-portal/event/btw2021"
namespaces = ["confref-portal"]
kind = "records"
method = ["converted"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/confref-portal"
+++

The 37,945 conferences of 5,668 series of portal.confref.org (2019-2022), the prototype of confref built with the
Digital Science Catalyst Grant, as its API delivered them on 2020-07-11: name, acronym, place, year, dates, series
(with ISSN and DBLP id), research area and keywords. Mostly computer science, from the Springer Nature metadata API
(2002 on) and DBLP. The portal is offline; the download was kept by Wolfgang Fahl's ConferenceCorpus.

True to the API, with terms in the dataset namespace (`vocab/`). Known limits of the source: many dates are
placeholders (start and end on 1 January of the year, 6,365 events), some years are impossible (0, 19670), the
rankings were never filled.
