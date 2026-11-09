"""ls-places: the place of every event record of the sources, as a Wikidata item (decision 0018).

The mentions (places.py): the names of city, region and country in springer-lod, confref-portal and confident, the
items of wikidata (wdt:P276) and of the GND (the Wikidata item of the GND place), and the place in the titles of the
dblp proceedings. The event records are those of events.py and the events of the GND.

Rules, per mention, the most specific that applies:
1. item: the item the source names (Wikidata, GND), as it is.
2. city: the items whose label or alias in Wikidata (LANGUAGES of the harvest) is the city name, that have
   coordinates and lie in the country of the mention (wdt:P17). Of these the settlements (instances of a subclass of
   human settlement), else, if there is exactly one, the one item (a venue, a campus); among several the one with the
   most Wikipedia articles (sitelinks), then the lowest Q number. Without a country only a settlement with at least
   three times as many sitelinks as the next one.
3. region: a first-level subdivision of the country (ISO 3166-2) named as city or region.
4. country: the country.

Writes schema:location from the record to the item, and ls-places-matches.tsv.gz: every link with its rule, the
mention and the number of candidates.
"""

import gzip
import io
from collections import defaultdict

from cr import identifiers
from cr.generator import load_shared
from cr.rdf import IRI, RDF_TYPE, read_triples

events = load_shared("ls-springer-lod-events", "events")
places = load_shared("ls-places", "places")

INPUTS = {**events.INPUTS, "gnd": "gnd/2026-11-08", "harvest": "inputs:wikidata/places-2026-11-09"}
PARAMS = {}

SCHEMA_LOCATION = "http://schema.org/location"
GNDO = places.GNDO
ALIASES = {"springer": "springer", "portal": "portal", "confident": "confident", "wikidata": "wikidata",
           "dblp": "dblp", "gnd": "gnd"}


def harvest_file(run, name):
    for p in run.inputs("harvest"):
        if p.name == name:
            return p
    raise FileNotFoundError(name)


def load_harvest(run):
    """(gazetteer, {name: {item}}, {item: (sitelinks, settlement)}, {item: {country iso}}, {item: has coordinates})"""
    countries, subdivisions, names = {}, {}, defaultdict(set)
    for f in ("countries.nt", "country-labels.nt", "country-aliases.nt", "subdivisions.nt", "subdivision-labels.nt",
              "subdivision-aliases.nt"):
        for s, p, o in read_triples(harvest_file(run, f)):
            s = str(s)
            if p == places.W + "P297":
                countries[s] = o.value
            elif p == places.W + "P300":
                subdivisions.setdefault(s, [None, None])[0] = o.value
            elif p == places.W + "P17":
                subdivisions.setdefault(s, [None, None])[1] = str(o)
            else:
                names[s].add(o.value)
    c = {item: (code, sorted(names.get(item, ()))) for item, code in countries.items()}
    sd = {item: (code, countries.get(country), sorted(names.get(item, ())))
          for item, (code, country) in subdivisions.items() if code and country in countries}
    gaz = places.Gazetteer(c, sd)
    by_name = defaultdict(set)   # the names as harvested, and in the form of places.key
    for f in ("names-labels.tsv", "names-aliases.tsv"):
        for line in harvest_file(run, f).read_text(encoding="utf-8").splitlines()[1:]:
            name, _lang, item = line.split("\t")
            by_name[name].add(item)
            by_name["\0" + places.key(name)].add(item)
    facts = {}
    for line in harvest_file(run, "candidates.tsv").read_text(encoding="utf-8").splitlines()[1:]:
        item, sl, settle = line.split("\t")
        facts[item] = (int(sl or 0), settle == "1")
    in_country, coords = defaultdict(set), set()
    for s, p, o in read_triples(harvest_file(run, "statements.nt")):
        if p == places.W + "P17" and str(o) in countries:
            in_country[str(s)].add(countries[str(o)])
        elif p == places.W + "P625":
            coords.add(str(s))
    return gaz, by_name, facts, in_country, coords


def qnum(item):
    try:
        return int(item.rsplit("Q", 1)[1])
    except (IndexError, ValueError):
        return 1 << 60


def choose(name, isos, by_name, facts, in_country, coords, big, countries):
    """(item, rule, number of candidates) for a city name, or None. The candidates are ranked by their sitelinks
    (the number of Wikipedia articles), times 1.5 for a settlement and times 0.5 for a country or first-level
    subdivision, times 0.25 for a country (a city name is rather a city); ties by the lower Q number."""
    cands = [i for i in by_name.get(name) or by_name.get("\0" + places.key(name), ()) if i in coords]
    if isos:
        cands = [i for i in cands if in_country.get(i, set()) & isos]
    if not cands:
        return None

    def score(i):
        sl, settle = facts.get(i, (0, False))
        return (sl + 1) * (1.5 if settle else 1.0) * (0.25 if i in countries else 0.5 if i in big else 1.0)

    order = sorted(cands, key=lambda i: (-score(i), qnum(i)))
    best = order[0]
    rule = "region" if best in big and not facts.get(best, (0, False))[1] else "city"
    if isos:
        return best, rule, len(cands)
    if len(order) == 1 or score(best) >= 3 * score(order[1]):
        return best, rule + " (no country; clearly the best known)", len(cands)
    return None


def generate(run):
    gaz, by_name, facts, in_country, coords = load_harvest(run)
    country_items = set(gaz.country_item.values())
    big = country_items | {i for items in gaz.subdivision.values() for i in items}
    _uf, evs = events.read(run)
    known = {}
    for x, e in evs.items():
        known[x] = e.iri
        for part in e.extra if e.source == "dblp-event" else ():
            y = identifiers.identify(part)
            if y:
                known[y] = e.iri
    for s, p, o in run.triples("gnd"):
        if p == RDF_TYPE and str(o) == GNDO + "ConferenceOrEvent":
            x = identifiers.identify(s)
            if x:
                known[x] = str(s)

    def event_iri(_source, iri):
        x = identifiers.identify(iri)
        return known.get(x) if x else None

    def triples(name):
        return run.triples(ALIASES[name])

    ments = places.mentions(triples, gaz, event_iri)
    links, rows = set(), []
    counts = defaultdict(int)
    for rec in sorted(ments):
        for m in ments[rec]:
            got = None
            if m.item:
                got = (m.item, "item (" + m.how + ")", 1)
            used = m.city
            # the part before a region is tried first ("Monterey, California, USA"); then the region-like part as a
            # city ("Rome, Italy": Rome is also a region)
            for city in ((m.alt, m.city) if m.alt and m.region == m.city else (m.city, m.alt)):
                if not got and city:
                    got = choose(city, m.countries, by_name, facts, in_country, coords, big, country_items)
                    used = city
            if not got:
                for n in (m.region, m.city):
                    regions = {i for iso in m.countries for i in gaz.subdivision.get((places.key(n), iso), ())} if n \
                        else set()
                    if len(regions) == 1:
                        got = (regions.pop(), "region", 1)
                        break
            if not got and len(m.countries) == 1:
                iso = next(iter(m.countries))
                if iso in gaz.country_item:
                    got = (gaz.country_item[iso], "country", 1)
            counts[(m.source, got[1].split(" (")[0] if got else "none")] += 1
            if got:
                links.add((IRI(rec), IRI(SCHEMA_LOCATION), IRI(got[0])))
                rows.append("\t".join((rec, m.source, used, m.region, ",".join(sorted(m.countries)),
                                       "online" if m.online else "", got[0], got[1], str(got[2]))))
    head = "record\tsource\tcity\tregion\tcountry\tonline\tplace\trule\tcandidates"
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as f:
        f.write(("\n".join([head] + sorted(set(rows))) + "\n").encode("utf-8"))
    run.path("ls-places-matches.tsv.gz").write_bytes(buf.getvalue())
    by_source = defaultdict(dict)
    for (src, rule), n in counts.items():
        by_source[src][rule] = n
    run.note(f"{len(ments):,} event records with a place mention; {len(links):,} links. Per source and rule: "
             + "; ".join(f"{s}: " + ", ".join(f"{r} {n:,}" for r, n in sorted(d.items()))
                         for s, d in sorted(by_source.items())) + ".")
    run.write_turtle("ls-places.ttl.gz", links)
