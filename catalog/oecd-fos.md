+++
slug = "oecd-fos"
title = "Fields of science and technology (OECD FOS 2007)"
author = "Kai Eckert"
website = "https://www.oecd.org/science/inno/38235147.pdf"
example = "https://id.confref.org/data/oecd-fos/1.2"
stable = "2026-11-09"
kind = "vocabulary"
method = ["curated"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/oecd-fos"

[[versions]]
version = "2026-11-09"
issued = "2026-11-09"
author = "Kai Eckert"
commit = "cc4a2b86e138b56019be50fea2c073b789684af9"
description = "The 6 major fields and 42 fields of the OECD classification of fields of science and technology (2007), with English and German names."

  [[versions.files]]
  path = "oecd-fos.ttl.gz"
  bytes = 1866
  sha256 = "aeed45461d54e2fd9df40cc8f96bf7b85f3de35d331fd8e8533ad978c1647dac"
  triples = 340

  [[versions.files]]
  path = "oecd-fos-meta.ttl.gz"
  bytes = 1512
  sha256 = "28b05d57e75a16e0bcde127e9148a21c2ba025d2e88e71307345a1fe45b1f3d7"
  triples = 61

[[changelog]]
date = "2026-11-09"
version = "2026-11-09"
author = "Kai Eckert"
text = "New version, made by the generator in confref-data (run-20261109T074906Z)."
+++

The fields of science and technology of the OECD (Frascati Manual, revised 2007) as SKOS concepts: 6 major fields
and 42 fields, with their codes and their English and German names. They are the academic fields of confref: the
fields of the sources are mapped to them in `ls-fields`. ConfIDent uses the same classification.
