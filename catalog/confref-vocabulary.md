+++
slug = "confref-vocabulary"
title = "confref dataset vocabulary"
author = "Kai Eckert"
example = "https://id.confref.org/datasets/vocabulary/kind/linkset"
stable = "2026-11-09"
kind = "vocabulary"
method = ["curated"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/confref-vocabulary"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "76d24c62773de9473b537b9ef808dbd076c3d090"
description = "The kinds and methods of catalog/vocabulary.toml."

  [[versions.files]]
  path = "confref-vocabulary.ttl.gz"
  bytes = 2257
  sha256 = "5767ab2d26ca669a1b20c791842edd74e741055b5f2558b6235ae38c8dec2320"
  triples = 154

  [[versions.files]]
  path = "confref-vocabulary-meta.ttl.gz"
  bytes = 1428
  sha256 = "b03453affbcf3bb8d0ff3ad114f9866dc3ea096c44e90d8e3142fbe1244a6c1b"
  triples = 59

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "First version."
+++

The values of the catalogue fields `kind` and `method` as SKOS concepts, generated from `catalog/vocabulary.toml`:
what a dataset is (records, authority data, linkset, ratings and others) and how it was made. The description of
every dataset names them as its types (`dcterms:type`).
