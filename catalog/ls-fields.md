+++
slug = "ls-fields"
title = "Academic fields and disciplines of the series and events"
author = "Kai Eckert"
example = "https://dblp.org/streams/conf/semweb"
kind = "linkset"
method = ["deterministic", "rule-based", "curated"]
inputs = ["springer-lod", "confref-portal", "confident", "wikidata", "dblp", "ls-springer-lod-dblp", "oecd-fos"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/ls-fields"
+++

The academic fields (`cr:field`, the 42 fields of the OECD classification in `oecd-fos`) and the disciplines
(`cr:discipline`, Wikidata items) of the series and event records of the sources. ConfIDent states the field of each of
its academic fields; these are matched by name to Wikidata disciplines. The research areas of the portal are mapped by
hand. Wikidata names the main subject of many events. dblp is the bibliography of computer science, so its venues and
events are in computer and information sciences; Springer conferences get the field of the book series of their
proceedings. Each discipline gets a field as well. The file `ls-fields-disciplines.tsv.gz` lists the academic fields of
ConfIDent with the Wikidata item chosen for each.
