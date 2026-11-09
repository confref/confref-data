+++
slug = "confref-vocabulary"
title = "confref dataset vocabulary"
author = "Kai Eckert"
example = "https://id.confref.org/datasets/vocabulary/kind/linkset"
kind = "vocabulary"
method = ["curated"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/confref-vocabulary"
+++

The values of the catalogue fields `kind` and `method` as SKOS concepts, generated from `catalog/vocabulary.toml`:
what a dataset is (records, authority data, linkset, ratings and others) and how it was made. The description of
every dataset names them as its types (`dcterms:type`).
