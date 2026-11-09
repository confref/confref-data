+++
slug = "ls-places"
title = "Places of the events, as Wikidata items"
author = "Kai Eckert"
example = "http://lod.springer.com/data/conference/3dph2009"
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
+++

The place of each event record of the sources, as a Wikidata item (`schema:location`). Where a source names a
Wikidata item (Wikidata, and the GND through the Wikidata item of its place), the item is taken as it is. The names of
city, region and country (Springer, the portal, ConfIDent, and the titles of the dblp proceedings) are looked up in
Wikidata: a city name in the country of the event, preferring settlements and, among several, the best known (the
most Wikipedia articles). Where no city is found, the region or the country. The file `ls-places-matches.tsv.gz` lists
every link with the mention it comes from, its rule and the number of candidates.
