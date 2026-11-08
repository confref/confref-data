+++
slug = "gnd"
title = "GND: the conferences, series and places our datasets name"
author = "Kai Eckert"
website = "https://gnd.network/"
example = "https://d-nb.info/gnd/1060089858"
stable = "2026-11-08"
kind = "authority"
method = ["lookup"]
inputs = ["springer-lod", "dblp", "wikidata"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"owl:sameAs" = ["wikidata"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Gemeinsame Normdatei (GND), Deutsche Nationalbibliothek (https://d-nb.info/gnd/)"
statement = "https://d-nb.info/gnd/1060089858/about/lds"   # every record states dcterms:license CC0 in its description

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/gnd"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "af1b4260e0ab0751f19e6b8b6b956f4c386aa992"
description = "The 11,472 GND records named by the stable versions 2026-11-08 of springer-lod, dblp and wikidata (9,618 numbers) or by these records as place or related conference (1,855), fetched from the Linked Data Service of the DNB on 2026-11-08; 4 replaced numbers, none unknown."

  [[versions.files]]
  path = "gnd-selection.tsv.gz"
  bytes = 80492
  sha256 = "35ff639a70dbd3ae904c9071d21db0aca3f228f8c70a647e3152fe9c593d666e"

  [[versions.files]]
  path = "gnd.ttl.gz"
  bytes = 1091491
  sha256 = "e88ff79b6eea01d469972502de8770ec884770b5c26ade989a4e49a80c1bb7c4"
  triples = 133545

  [[versions.files]]
  path = "gnd-meta.ttl.gz"
  bytes = 2277
  sha256 = "8fa779a115502324cf2874a3602ef5c3eee522cf291cadff1c5ca98fd2d7d556"
  triples = 87

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T213929Z)."
+++

The records of the Integrated Authority File (GND) of the German National Library that confref's datasets name: the
conferences and conference series linked by the Springer data (5,838), by Wikidata (its GND IDs) and by dblp, and,
one step further, the places and related conferences these records name. As the DNB states them (names with number,
year and place, dates, places, related events, links to VIAF and the Library of Congress), with the replaced and
unknown numbers. The GND is linked, not taken over: its other conferences are not in confref (decision 0001).
