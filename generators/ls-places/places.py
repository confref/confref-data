"""The places the sources name for their events, and how names are matched to Wikidata places (shared by the
harvest and the generator of ls-places, and by the generator of wikidata-places).

Mentions, per event record (the records of events.py, decision 0013):
- springer-lod: spr:confCity and spr:confCountry (names);
- confref-portal: portal:city and portal:country (names);
- confident: cf:City (a name), cf:Region (a name), cf:Country (a country page, "Country:JP": the ISO code);
- wikidata: wdt:P276 (location) and wdt:P17 (country), Wikidata items;
- gnd: gndo:placeOfConferenceOrEvent, a GND place, and the Wikidata item the GND states for it (owl:sameAs);
- dblp: the titles of the proceedings of an event, "…, Bled, Slovenia, June 3-5, 2015, Proceedings": the last part
  that names a country, the part before it as the city, or as a region (a first-level subdivision of the country, a
  US state "CA") with the city before it; "Virtual Event" marks an online event.

Countries are recognised by their names in Wikidata (labels and aliases of the items with an ISO 3166-1 code,
wdt:P297), by COUNTRY_NAMES (names the sources use that Wikidata does not have) and, for historical states, by
FORMER (the present countries their cities are looked up in).
"""

import re
import unicodedata
from collections import defaultdict

from cr import identifiers
from cr.rdf import RDF_TYPE, Literal

SPR = "http://lod.springer.com/data/ontology/property/"
PORTAL = "https://id.confref.org/data/confref-portal/vocab/"
CF = "https://id.confref.org/data/confident/vocab/"
W = "http://www.wikidata.org/prop/direct/"
WD = "http://www.wikidata.org/entity/"
DBLP = "https://dblp.org/rdf/schema#"
GNDO = "https://d-nb.info/standards/elementset/gnd#"
SAME = "http://www.w3.org/2002/07/owl#sameAs"

# names of countries in the sources that are neither labels nor aliases of the country in Wikidata
COUNTRY_NAMES = {
    "usa": "US", "u.s.a.": "US", "us": "US", "united states of america": "US", "uk": "GB", "u.k.": "GB",
    "england": "GB", "scotland": "GB", "wales": "GB", "northern ireland": "GB", "great britain": "GB",
    "korea": "KR", "republic of korea": "KR", "south korea": "KR", "the netherlands": "NL", "holland": "NL",
    "czech republic": "CZ", "russia": "RU", "russian federation": "RU", "taiwan": "TW", "r.o.c.": "TW",
    "roc": "TW", "p.r. china": "CN", "pr china": "CN", "p. r. china": "CN", "prc": "CN", "hong kong": "HK",
    "macau": "MO", "macao": "MO", "vietnam": "VN", "viet nam": "VN", "iran": "IR", "uae": "AE",
    "u.a.e.": "AE", "turkiye": "TR", "türkiye": "TR", "slovak republic": "SK", "brasil": "BR",
    "the philippines": "PH", "frg": "DE", "west germany": "DE", "f.r. germany": "DE",
    "federal republic of germany": "DE", "puerto rico": "PR", "ivory coast": "CI", "macedonia": "MK",
    "fyr macedonia": "MK", "bosnia": "BA", "the bahamas": "BS", "kingdom of saudi arabia": "SA", "ksa": "SA",
    "korea (republic of)": "KR", "north cyprus": "CY", "tahiti": "PF",
    # misspellings in the portal
    "the netherland": "NL", "brazill": "BR", "new zeeland": "NZ", "cannada": "CA", "morocc": "MA",
    "switerland": "CH", "singagore": "SG",
}
# historical states: the present countries their places are in
FORMER = {"czechoslovakia": ("CZ", "SK"), "ussr": ("RU", "UA", "BY", "EE", "LV", "LT", "GE", "AM", "AZ", "KZ",
                                                   "UZ", "KG", "TJ", "TM", "MD"),
          "soviet union": ("RU", "UA", "BY", "EE", "LV", "LT", "GE", "AM", "AZ", "KZ", "UZ", "KG", "TJ", "TM", "MD"),
          "yugoslavia": ("RS", "HR", "SI", "BA", "MK", "ME", "XK"), "gdr": ("DE",), "east germany": ("DE",),
          "ddr": ("DE",)}
ONLINE = {"virtual event", "virtual", "online", "virtual conference", "online event", "virtual meeting"}
MONTHS = r"(?:jan|feb|mar|apr|may|jun|jul|aug|sep|oct|nov|dec)[a-z]*\.?"


def key(name):
    """The form in which names are compared: case-folded, without accents, dots and a leading "the"."""
    s = unicodedata.normalize("NFKD", name or "")
    s = "".join(c for c in s if not unicodedata.combining(c)).casefold()
    s = re.sub(r"[.’']", "", s.replace("ß", "ss"))
    s = re.sub(r"[\s\-_]+", " ", s).strip()
    return s[4:] if s.startswith("the ") else s


class Gazetteer:
    """Countries and their first-level subdivisions, from the harvest."""

    def __init__(self, countries, subdivisions):
        # countries: {item: (iso, [names])}; subdivisions: {item: (iso 3166-2 code, country iso, [names])}
        self.country_item = {iso: item for item, (iso, _n) in countries.items()}
        self.iso = {item: iso for item, (iso, _n) in countries.items()}
        self.country = defaultdict(set)   # key -> {iso}
        for item, (iso, names) in countries.items():
            for n in names:
                self.country[key(n)].add(iso)
        for n, iso in COUNTRY_NAMES.items():
            self.country[key(n)] = {iso}
        for n, isos in FORMER.items():
            self.country[key(n)] = set(isos)
        self.subdivision = defaultdict(set)   # (key, country iso) -> {item}
        self.region_country = defaultdict(set)   # key -> {country iso}, for "San Jose, CA" without a country
        self.region_any = defaultdict(set)   # key of any name of a subdivision -> {country iso}
        for item, (code, iso, names) in subdivisions.items():
            short = code.split("-", 1)[1] if "-" in code else ""
            for n in set(names) | ({short} if iso in ("US", "CA", "AU", "IN", "BR", "MX") and short else set()):
                self.subdivision[(key(n), iso)].add(item)
                self.region_any[key(n)].add(iso)
                if iso in ("US", "CA", "AU") and n == short:
                    self.region_country[key(n)].add(iso)

    def countries(self, name):
        return self.country.get(key(name), set())

    def place(self, city, country):
        """(city, region, {country iso}) from a city and a country field: a country field that names no country
        may name a region of one country ("California") or the city itself ("München")."""
        isos = self.countries(country)
        if isos or not country:
            return city, "", isos
        regions = self.region_any.get(key(country), set())
        if len(regions) == 1:
            return city, country, set(regions)
        return (city or country), "", set()

    def is_region(self, name, isos):
        return any((key(name), iso) in self.subdivision for iso in isos)


def clean_city(name):
    """A city name as written in the sources, without a trailing region ("Santa Fe, NM" -> "Santa Fe")."""
    name = re.sub(r"\s+", " ", (name or "").strip(" ,;"))
    return name.split(",")[0].strip() if "," in name else name


def parse_title(title, gaz):
    """(city, alternative city, region, {country iso}, online) from the title of a proceedings volume, or None. The
    part before the country is the city; if it also names a region of the country (a US state "CA", but also
    "Rome" or "Kyoto", which are cities and regions), the part before it is the alternative city, tried when the
    first is not found as a city."""
    parts = [p.strip(" .") for p in re.split(r",|\(|\)|;", title or "")]
    parts = [p for p in parts if p]
    online = any(key(p) in ONLINE for p in parts)

    def usable(city):
        return city and key(city) not in ONLINE and not re.search(r"\d", city) \
            and not re.match(MONTHS + r"$", key(city)) and not re.fullmatch(r"[A-Z]{2}", city)

    for i in range(len(parts) - 1, 0, -1):
        isos = gaz.countries(parts[i])
        if not isos:
            continue
        city, alt, region = parts[i - 1], "", ""
        if gaz.is_region(city, isos):
            region = city
            alt = parts[i - 2] if i >= 2 else ""
        return (city if usable(city) else ""), (alt if usable(alt) else ""), region, isos, online
    for i in range(len(parts) - 1, 0, -1):   # "San Jose, CA, January 28, 1996": a US state without the country
        isos = gaz.region_country.get(key(parts[i]))
        if isos and re.search(r"\d|" + MONTHS, key(" ".join(parts[i + 1:i + 2]))):
            city = parts[i - 1]
            if usable(city):
                return city, "", parts[i], set(isos), online
    return ("", "", "", set(), True) if online else None


class Mention:
    __slots__ = ("source", "city", "alt", "region", "countries", "item", "online", "how")

    def __init__(self, source, city="", region="", countries=(), item="", online=False, how="", alt=""):
        self.source, self.city, self.alt, self.region = source, city, alt, region
        self.countries, self.item, self.online, self.how = set(countries), item, online, how


def val(o):
    return o.value if isinstance(o, Literal) else str(o)


def mentions(triples, gaz, event_iri):
    """{event record IRI: [Mention]} for the event records of the sources. triples(name) yields the triples of an
    input (names as in events.INPUTS plus "gnd"); event_iri(source, iri) gives the record IRI under which events.py
    knows an event (the first part of a dblp event), or None for a record that is not an event there."""
    out = defaultdict(list)

    def add(source, s, m):
        x = event_iri(source, str(s))
        if x:
            out[x].append(m)

    d = defaultdict(dict)
    for s, p, o in triples("springer"):
        if p in (SPR + "confCity", SPR + "confCountry") and str(s).startswith("http://lod.springer.com/data/conference/"):
            d[str(s)][p[len(SPR):]] = val(o)
    for s, f in d.items():
        city, region, isos = gaz.place(clean_city(f.get("confCity")), f.get("confCountry", ""))
        add("springer", s, Mention("springer-lod", city, region, isos, how="names"))
    d = defaultdict(dict)
    for s, p, o in triples("portal"):
        if p in (PORTAL + "city", PORTAL + "country") and "/confref-portal/event/" in str(s):
            d[str(s)][p[len(PORTAL):]] = val(o)
    for s, f in d.items():
        city, region, isos = gaz.place(clean_city(f.get("city")), f.get("country", ""))
        add("confref-portal", s, Mention("confref-portal", city, region, isos, how="names"))
    d, page = defaultdict(dict), {}
    for s, p, o in triples("confident"):
        if p in (CF + "City", CF + "Region", CF + "Country", CF + "Event_Mode"):
            d[str(s)][p[len(CF):]] = val(o)
        elif p == CF + "pageTitle" and val(o).startswith("Country:"):
            page[str(s)] = val(o)[len("Country:"):].strip().upper()
    for s, f in d.items():
        iso = page.get(f.get("Country", ""))
        city, region = clean_city(f.get("City")), f.get("Region", "")
        if city.count("/") == 2:   # "ES/SA/Salamanca": country, region code, city
            city = city.rsplit("/", 1)[1].strip()
        if key(city) in ("n/a", "na", "tba", "tbd", "online", "virtual"):
            city = ""
        add("confident", s, Mention("confident", city, region,
                                    {iso} if iso else set(), online=f.get("Event_Mode") == "online", how="names"))
    d = defaultdict(lambda: defaultdict(list))
    for s, p, o in triples("wikidata"):
        if p in (W + "P276", W + "P17"):
            d[str(s)][p].append(str(o))
    for s, f in d.items():
        for item in sorted(f.get(W + "P276", [])) or [""]:
            isos = {gaz.iso[c] for c in f.get(W + "P17", []) if c in gaz.iso}
            add("wikidata", s, Mention("wikidata", item=item, countries=isos, how="item"))
    gplace, gsame = defaultdict(list), defaultdict(list)
    for s, p, o in triples("gnd"):
        if p == GNDO + "placeOfConferenceOrEvent":
            gplace[str(s)].append(str(o))
        elif p == SAME and str(o).startswith(WD):
            gsame[str(s)].append(str(o))
    for s, places in gplace.items():
        for pl in sorted(places):
            for item in sorted(gsame.get(pl, [])):
                add("gnd", s, Mention("gnd", item=item, how="gnd place"))
    titles = dblp_titles(triples)
    for s, ts in titles.items():
        for t in sorted(ts):
            r = parse_title(t, gaz)
            if r:
                city, alt, region, isos, online = r
                add("dblp-event", s, Mention("dblp", city, region, isos, online=online, how="title", alt=alt))
                break
    return out


def dblp_titles(triples):
    """{table of contents IRI: [titles of its proceedings]}."""
    title, toc = {}, defaultdict(list)
    for s, p, o in triples("dblp"):
        if p == DBLP + "title":
            title[str(s)] = val(o)
        elif p == DBLP + "listedOnTocPage":
            toc[str(s)].append(str(o))
    out = defaultdict(list)
    for r, tocs in toc.items():
        if r in title:
            for t in tocs:
                out[t].append(title[r])
    return out


def names_to_look_up(ments):
    """The city and region names to look up in Wikidata."""
    names = set()
    for ms in ments.values():
        for m in ms:
            for n in (m.city, m.alt, m.region):
                if n and len(n) <= 80:
                    names.add(n)
    return names


def items_to_look_up(ments):
    return {m.item for ms in ments.values() for m in ms if m.item}


def identify(iri):
    return identifiers.identify(iri)
