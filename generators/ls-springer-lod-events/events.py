"""Matching the events of the sources within linked series (shared by the ls-*-events linksets).

1. Series clusters: the series records of the sources joined by the identity links that join (kg-commons 0032; the
   judged linkset ls-springer-lod-dblp for Springer): Springer series and dblp venues (ls-springer-lod-dblp), portal
   series and dblp venues (portal:dblpId), ConfIDent series and dblp venues and Wikidata (cf:DBLP_Series_ID,
   cf:Wikidata_Series_ID), Wikidata series and dblp venues (wdt:P8926), dblp venues and Wikidata (owl:sameAs).
2. Events and their series: Springer conferences (spr:hasSeries), portal events (portal:series), ConfIDent events
   (cf:In_Event_Series), Wikidata items with a series (wdt:P179) and a date that are not proceedings or series, and the
   events of dblp: the tables of contents (dblp:listedOnTocPage) of the proceedings published in a conference venue.
   Facts: year, edition number, start date, acronym, name, place. The year of a dblp event is the year in its key
   (eswc2016), else the most frequent year in the titles of its proceedings, else the year of publication; its number
   the ordinal in the titles ("13th").
3. Matching, per cluster and year, between the events of two sources:
   - only event: each source has one event of the cluster in that year, the cluster has at most one series record
     per source, and nothing contradicts (edition numbers both given and different; start dates more than 3 days
     apart; one of the two marked as the workshops of a conference by its acronym, "ICCBR-WS 2021", the other not);
   - agreement: otherwise, an event is matched to the one event of the other source that agrees with it (same edition
     number, start dates at most 1 day apart, or the same acronym, with or without its year) and with no other, and
     nothing contradicts.
"""

import re
from collections import Counter, defaultdict
from datetime import date

from cr import identifiers
from cr.rdf import RDF_TYPE, Literal

SPR = "http://lod.springer.com/data/ontology/property/"
PORTAL = "https://id.confref.org/data/confref-portal/vocab/"
CF = "https://id.confref.org/data/confident/vocab/"
W = "http://www.wikidata.org/prop/direct/"
WD = "http://www.wikidata.org/entity/"
DBLP = "https://dblp.org/rdf/schema#"
RDFS_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
SAME = "http://www.w3.org/2002/07/owl#sameAs"
CR_SAME = "https://id.confref.org/ontology/sameAs"
NOT_EVENTS = {WD + "Q1143604", WD + "Q47258130", WD + "Q13442814", WD + "Q5633421", WD + "Q3331189"}

SOURCES = ["springer", "confref-portal", "confident", "wikidata", "dblp-event"]   # the order of the links: earlier
# sources link to later ones
INPUTS = {"springer": "springer-lod/2026-11-08", "portal": "confref-portal/2026-11-09",
          "confident": "confident/2026-11-08", "wikidata": "wikidata/2026-11-08", "dblp": "dblp/2026-11-08",
          "ls_springer_dblp": "ls-springer-lod-dblp/2026-11-09"}
SLUGS = {"springer": "springer-lod", "portal": "confref-portal", "confident": "confident", "wikidata": "wikidata",
         "dblp": "dblp", "ls_springer_dblp": "ls-springer-lod-dblp"}


def val(o):
    return o.value if isinstance(o, Literal) else str(o)


def year_of(v):
    m = re.match(r"^\s*([12][0-9]{3})", v or "")
    return int(m.group(1)) if m else None


def day_of(v):
    m = re.match(r"^\s*([12][0-9]{3})-([01][0-9])-([0-3][0-9])", v or "")
    try:
        return date(int(m.group(1)), int(m.group(2)), int(m.group(3))) if m else None
    except ValueError:
        return None


def number_of(v):
    m = re.match(r"^\s*([0-9]+)", v or "")
    return int(m.group(1)) if m else None


def norm_acronym(v):
    return re.sub(r"[^a-z0-9]", "", (v or "").lower())


class UnionFind:
    def __init__(self):
        self.parent = {}

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def union(self, a, b):
        self.parent[self.find(a)] = self.find(b)


class Event:
    __slots__ = ("source", "ident", "iri", "series", "year", "number", "start", "acronym", "name", "place", "extra")

    def __init__(self, source, ident, iri):
        self.source, self.ident, self.iri = source, ident, iri
        self.series, self.year, self.number, self.start = set(), None, None, None
        self.acronym, self.name, self.place, self.extra = "", "", "", set()

    def facts(self):
        return {"year": self.year, "number": self.number, "start": self.start.isoformat() if self.start else None,
                "acronym": self.acronym, "name": self.name, "place": self.place}


def node(term, predicate=None):
    x = identifiers.identify(term, predicate)
    return x if x else None


def read(run):
    """(series clusters, events): uf over series nodes (source, id), events {(source, id): Event}."""
    uf = UnionFind()
    joins = identifiers.joins

    def link(slug, s, p, o, want):
        a, b = node(s), node(o, p)
        if a and b and b[0] in want and joins(slug, p, b[0]):
            uf.union(a, b)

    events = {}

    def event(source, s):
        x = node(s)
        if not x:
            return None
        if x not in events:
            events[x] = Event(source, x[1], str(s))
        return events[x]

    # Springer
    for s, p, o in run.triples("ls_springer_dblp"):
        link("ls-springer-lod-dblp", s, p, o, {"dblp-venue"})
    for s, p, o in run.triples("springer"):
        if str(s).startswith("http://lod.springer.com/data/conference/"):
            e = event("springer", s)
            if p == SPR + "hasSeries":
                e.series.add(node(o))
            elif p == SPR + "confYear":
                e.year = year_of(val(o))
            elif p == SPR + "confNumber":
                e.number = number_of(val(o))
            elif p == SPR + "confStartDate":
                e.start = day_of(val(o))
            elif p == SPR + "confAcronym":
                e.acronym = val(o)
            elif p == SPR + "confName":
                e.name = val(o)
            elif p == SPR + "confCity":
                e.place = val(o)
    # the portal
    for s, p, o in run.triples("portal"):
        if p == PORTAL + "dblpId":
            link("confref-portal", s, p, o, {"dblp-venue"})
        elif "/confref-portal/event/" in str(s):
            e = event("confref-portal", s)
            if p == PORTAL + "series":
                e.series.add(node(o))
            elif p == PORTAL + "year":
                e.year = year_of(val(o))
            elif p == PORTAL + "startDate":
                e.start = day_of(val(o))
            elif p == PORTAL + "acronym":
                e.acronym = val(o)
            elif p == PORTAL + "name":
                e.name = val(o)
            elif p == PORTAL + "city":
                e.place = val(o)
    # ConfIDent
    cf_class = {}
    cf = defaultdict(list)
    for s, p, o in run.triples("confident"):
        if p in (CF + "DBLP_Series_ID", CF + "Wikidata_Series_ID"):
            link("confident", s, p, o, {"dblp-venue", "wikidata"})
        elif p == RDF_TYPE:
            cf_class[str(s)] = str(o)
        elif p in (CF + "In_Event_Series", CF + "Year", CF + "Ordinal", CF + "Start_Date", CF + "Acronym",
                   CF + "Title", CF + "City"):
            cf[str(s)].append((p, o))
    for s, facts in cf.items():
        if cf_class.get(s) != CF + "Category_Event":
            continue
        e = event("confident", s)
        for p, o in facts:
            k = p[len(CF):]
            if k == "In_Event_Series" and not isinstance(o, Literal):
                e.series.add(node(o))
            elif k == "Year":
                e.year = year_of(val(o))
            elif k == "Ordinal":
                e.number = number_of(val(o))
            elif k == "Start_Date":
                e.start = day_of(val(o))
            elif k == "Acronym":
                e.acronym = val(o)
            elif k == "Title":
                e.name = val(o)
            elif k == "City":
                e.place = val(o)
    # Wikidata
    wd = defaultdict(lambda: defaultdict(list))
    for s, p, o in run.triples("wikidata"):
        if p == W + "P8926":
            link("wikidata", s, p, o, {"dblp-venue"})
        elif p in (W + "P179", W + "P31", W + "P580", W + "P585", W + "P393", W + "P1813", W + "P10692", W + "P276") \
                or (p == RDFS_LABEL and isinstance(o, Literal) and o.lang in ("en", "mul")):
            wd[str(s)][p].append(o)
    for s, f in wd.items():
        if not f.get(W + "P179") or set(map(str, f.get(W + "P31", []))) & NOT_EVENTS:
            continue
        start = [val(o) for o in f.get(W + "P580", []) + f.get(W + "P585", [])]
        if not start:
            continue
        e = event("wikidata", s)
        e.series = {node(o) for o in f[W + "P179"]}
        e.year, e.start = year_of(start[0]), day_of(start[0])
        e.number = number_of(val(f[W + "P393"][0])) if f.get(W + "P393") else None
        e.acronym = val(f[W + "P1813"][0]) if f.get(W + "P1813") else ""
        e.name = val(f[RDFS_LABEL][0]) if f.get(RDFS_LABEL) else ""
        e.place = val(f[W + "P276"][0]).rsplit("/", 1)[-1] if f.get(W + "P276") else ""
        if f.get(W + "P10692"):
            e.extra.add("has-dblp-event")
    # dblp
    toc = defaultdict(lambda: {"venues": set(), "titles": [], "years": []})
    rec = defaultdict(dict)
    for s, p, o in run.triples("dblp"):
        if p == SAME and str(s).startswith("https://dblp.org/streams/"):
            link("dblp", s, p, o, {"wikidata"})
        elif p == DBLP + "listedOnTocPage":
            rec[str(s)].setdefault("toc", []).append(o)
        elif p == DBLP + "publishedInStream":
            rec[str(s)].setdefault("venues", []).append(o)
        elif p == DBLP + "title":
            rec[str(s)]["title"] = val(o)
        elif p == DBLP + "yearOfPublication":
            rec[str(s)]["year"] = year_of(val(o))
    for r in rec.values():
        for t in r.get("toc", []):
            x = node(t)
            if not x or x[0] != "dblp-event":
                continue
            d = toc[x]
            d["venues"] |= {v for v in (node(o) for o in r.get("venues", [])) if v and v[1].startswith("conf/")}
            if r.get("title"):
                d["titles"].append(r["title"])
            if r.get("year"):
                d["years"].append(r["year"])
    for x, d in toc.items():
        if not d["venues"]:
            continue
        e = Event("dblp-event", x[1], "https://dblp.org/db/" + x[1])
        events[x] = e
        e.series = set(d["venues"])
        m = re.search(r"(19[5-9][0-9]|20[0-9]{2})", x[1].rsplit("/", 1)[-1])
        title_years = Counter(int(y) for t in d["titles"] for y in re.findall(r"\b(19[5-9][0-9]|20[0-9]{2})\b", t))
        e.year = int(m.group(1)) if m else (title_years.most_common(1)[0][0] if title_years else
                                              (min(d["years"]) if d["years"] else None))
        nums = Counter(int(n) for t in d["titles"] for n in re.findall(r"\b([0-9]{1,3})(?:st|nd|rd|th)\b", t))
        e.number = nums.most_common(1)[0][0] if nums else None
        e.name = sorted(d["titles"])[0] if d["titles"] else ""
        e.acronym = x[1].rsplit("/", 1)[-1]
    for e in events.values():
        e.series.discard(None)
    return uf, events


WORKSHOPS_ACRONYM = re.compile(r"[\s-]WS(?:\b|[0-9])", re.I)   # ICCBR-WS 2021


def workshops(e):
    """Whether an event is marked as the workshops of a conference by its acronym ("ICCBR-WS 2021"). Not the key of
    a dblp event (dhandnlp-ws2020 is a workshop series of its own) and not "Workshops" in a name: many events publish
    "Workshops" proceedings themselves (JSAI-isAI, LWDA, AICOL)."""
    return e.source != "dblp-event" and bool(WORKSHOPS_ACRONYM.search(e.acronym or ""))


def contradicts(a, b):
    if a.number and b.number and a.number != b.number:
        return True
    if workshops(a) != workshops(b):   # the workshops of a conference are not the conference
        return True
    return bool(a.start and b.start and abs((a.start - b.start).days) > 3)


def agrees(a, b):
    if a.number and b.number and a.number == b.number:
        return True
    if a.start and b.start and abs((a.start - b.start).days) <= 1:
        return True
    x, y = norm_acronym(a.acronym), norm_acronym(b.acronym)   # an acronym with or without its year
    return bool(x and y) and (x == y or (a.year and x + str(a.year) == y) or (b.year and y + str(b.year) == x))


def match(uf, events):
    """[(event a, event b, rule)] for every pair of sources in SOURCES order (a earlier), deduplicated."""
    by = defaultdict(lambda: defaultdict(list))   # (cluster, year) -> source -> [events]
    members = defaultdict(set)                    # cluster -> {series nodes}
    for x, e in events.items():
        if e.year is None:
            continue
        for sn in e.series:
            c = uf.find(sn)
            members[c].add(sn)
            if e not in by[(c, e.year)][e.source]:
                by[(c, e.year)][e.source].append(e)
    for sn in list(uf.parent):
        members[uf.find(sn)].add(sn)
    clean = {c for c, ms in members.items()
             if all(n <= 1 for n in Counter(m[0] for m in ms).values())}
    out = {}
    for (c, y), per in by.items():
        for i, sa in enumerate(SOURCES):
            for sb in SOURCES[i + 1:]:
                A, B = per.get(sa, []), per.get(sb, [])
                if not A or not B:
                    continue
                if len(A) == 1 and len(B) == 1 and c in clean:
                    a, b = A[0], B[0]
                    if not contradicts(a, b):
                        out.setdefault((a.iri, b.iri), (a, b, "only event of the series in the year"))
                    continue
                pairs = [(a, b) for a in A for b in B if agrees(a, b) and not contradicts(a, b)]
                ca, cb = Counter(id(a) for a, _ in pairs), Counter(id(b) for _, b in pairs)
                for a, b in pairs:
                    if ca[id(a)] == 1 and cb[id(b)] == 1:
                        out.setdefault((a.iri, b.iri), (a, b, "agrees in number, date or acronym"))
    return sorted(out.values(), key=lambda t: (t[0].iri, t[1].iri))
