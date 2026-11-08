+++
slug = "wikidata"
title = "Wikidata: academic conferences, conference series and proceedings"
author = "Kai Eckert"
website = "https://www.wikidata.org/"
example = "http://www.wikidata.org/entity/Q17012957"
stable = "2026-11-08"
kind = "records"
method = ["converted"]

[identity]   # the properties that state identity, and towards which sources (kg-commons 0032)
"wdt:P8926" = ["dblp-venue"]        # series
"wdt:P10692" = ["dblp-event"]       # events (the key of the table of contents)
"wdt:P227" = ["gnd"]                # events and series
"wdt:P8978" = ["dblp-rec"]          # proceedings
"wdt:P356" = ["doi"]                # proceedings
"wdt:P5124" = ["wikicfp-event"]
"wdt:P5127" = ["wikicfp-series"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Wikidata (https://www.wikidata.org)"
statement = "https://www.wikidata.org/wiki/Wikidata:Licensing"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/wikidata"

[[versions]]
version = "2026-11-08"
issued = "2026-11-08"
author = "Kai Eckert"
commit = "cc4d6ff12f9133b526435b06c6e951e3c0ed254a"
description = "The conferences, conference series and proceedings of Wikidata as on 2026-11-08, true to the source."

  [[versions.files]]
  path = "wikidata.ttl.gz"
  bytes = 2980130
  sha256 = "24690ef858082821465685960d248dce39afd46cec406f5a5cafd56c1c5f5422"
  triples = 405837

  [[versions.files]]
  path = "wikidata-meta.ttl.gz"
  bytes = 1912
  sha256 = "b886fcf1fc679bb293c06ee5e6313b8945bd6f08266329a5fc73337f318c3d4c"
  triples = 64

[[changelog]]
date = "2026-11-08"
version = "2026-11-08"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261108T193259Z)."
+++

The conferences of Wikidata: 35,271 items that are academic conferences or workshops, academic conference series,
carry an identifier of a conference or series (dblp, WikiCFP, KISTI, ACM) or are the proceedings of an event, with
all their truthy statements (dates, places, series, organisers, subjects, the conference identifiers and many
more), and their labels, aliases and descriptions in English, German and for all languages. Wikidata is the hub of
the identifiers of conferences; this is also the set confref will give its links back to.
