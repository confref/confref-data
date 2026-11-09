+++
slug = "ls-places"
title = "Places of the events, as Wikidata items"
author = "Kai Eckert"
example = "http://lod.springer.com/data/conference/3dph2009"
stable = "2026-11-09"
kind = "linkset"
method = ["deterministic", "rule-based"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "gnd", "ls-springer-lod-dblp"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-places"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "The places of 139,680 event records as Wikidata items (135,709 links), from the items of Wikidata and the GND and the place names of springer-lod, confref-portal, confident and the dblp titles."

  [[versions.files]]
  path = "ls-places-matches.tsv.gz"
  bytes = 1508426
  sha256 = "dcdac727d98f8b3e7af31d6ddcacd740d77b4dc20aa127fcdf63dfddd387d441"

  [[versions.files]]
  path = "ls-places.ttl.gz"
  bytes = 809812
  sha256 = "a1505117bb7cc09c9cb34f5c4f3e706ed3d0a81519d1290791fa9804af9305fb"
  triples = 135709

  [[versions.files]]
  path = "ls-places-meta.ttl.gz"
  bytes = 2491
  sha256 = "804ab055bd13952e33b34ee8cf6a8c40c54e0b0bc41a281073804ebabef62023"
  triples = 92

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T074911Z)."
+++

The place of each event record of the sources, as a Wikidata item (`schema:location`). Where a source names a
Wikidata item (Wikidata, and the GND through the Wikidata item of its place), the item is taken as it is. The names of
city, region and country (Springer, the portal, ConfIDent, and the titles of the dblp proceedings) are looked up in
Wikidata: a city name in the country of the event, preferring settlements and, among several, the best known (the
most Wikipedia articles). Where no city is found, the region or the country. The file `ls-places-matches.tsv.gz` lists
every link with the mention it comes from, its rule and the number of candidates.
