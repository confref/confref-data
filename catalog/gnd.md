+++
slug = "gnd"
title = "GND: the conferences, series and places our datasets name"
author = "Kai Eckert"
website = "https://gnd.network/"
example = "https://d-nb.info/gnd/1060089858"
kind = "authority"
method = ["lookup"]
inputs = ["springer-lod", "dblp", "wikidata"]

[license]
name = "CC0 1.0"
uri = "https://creativecommons.org/publicdomain/zero/1.0/"
image = "https://licensebuttons.net/p/zero/1.0/88x31.png"
attribution = "Gemeinsame Normdatei (GND), Deutsche Nationalbibliothek (https://d-nb.info/gnd/)"
statement = "https://d-nb.info/gnd/1060089858/about/lds"   # every record states dcterms:license CC0 in its description

[generator]
repo = "https://github.com/confref/confref-data"
path = "generators/gnd"
+++

The records of the Integrated Authority File (GND) of the German National Library that confref's datasets name: the
conferences and conference series linked by the Springer data (5,838), by Wikidata (its GND IDs) and by dblp, and,
one step further, the places and related conferences these records name. As the DNB states them (names with number,
year and place, dates, places, related events, links to VIAF and the Library of Congress), with the replaced and
unknown numbers. The GND is linked, not taken over: its other conferences are not in confref (decision 0001).
