+++
slug = "wikidata-disciplines"
title = "Wikidata: the disciplines of the series and events"
author = "Kai Eckert"
website = "https://www.wikidata.org/"
example = "http://www.wikidata.org/entity/Q21198"
stable = "2026-11-09"
kind = "records"
method = ["converted"]
inputs = ["ls-fields"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Wikidata (https://www.wikidata.org)"
statement = "https://www.wikidata.org/wiki/Wikidata:Licensing"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/wikidata-disciplines"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc69096c7b4a39c1d623d3b76b97c30b3994a6b2"
description = "The labels of the 1,536 Wikidata items that ls-fields 2026-11-09 names as disciplines."

  [[versions.files]]
  path = "wikidata-disciplines.ttl.gz"
  bytes = 29883
  sha256 = "c9004620e54c27f83fa1ced9b49b6faee61ceb487325252b89592b52d9e60884"
  triples = 2904

  [[versions.files]]
  path = "wikidata-disciplines-meta.ttl.gz"
  bytes = 1845
  sha256 = "a5ba9b99a26ff9a5cf6fd0544a076df37e27ca3d7f129496caa82dce6f996dec"
  triples = 64

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T075521Z)."
+++

The Wikidata items that `ls-fields` names as disciplines of series and events, with their labels in English, German
and for all languages. Their academic fields are in `ls-fields`.
