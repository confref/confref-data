+++
slug = "wikidata-places"
title = "Wikidata: the places of the events"
author = "Kai Eckert"
website = "https://www.wikidata.org/"
example = "http://www.wikidata.org/entity/Q437"
stable = "2026-11-09"
kind = "records"
method = ["converted"]
inputs = ["ls-places"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Wikidata (https://www.wikidata.org)"
statement = "https://www.wikidata.org/wiki/Wikidata:Licensing"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/wikidata-places"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "The 4,567 Wikidata items that ls-places 2026-11-09 names as places, and their 209 countries, with coordinates, country, class, administrative unit, ISO codes, population and labels."

  [[versions.files]]
  path = "wikidata-places.ttl.gz"
  bytes = 254922
  sha256 = "f3c4e55ad2e3169d33cf0483ffc59052e0f92050e7921d55c28e1e9b201f0804"
  triples = 40484

  [[versions.files]]
  path = "wikidata-places-meta.ttl.gz"
  bytes = 2000
  sha256 = "a9fd5ad15b6bad8ed5aef1e152d8c1dd149b21c8425d68bbfc30de778db2d947"
  triples = 65

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T075020Z)."
+++

The Wikidata items that `ls-places` names as the places of events (cities, regions, countries, some venues) and
their countries, as Wikidata states them: country, coordinates, class, the administrative unit they lie in, ISO
codes, population, and the labels in English, German and for all languages. The map and the place filters of the
platform are made from them.
