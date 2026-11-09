"""ids: the confref identifiers of conference series and events (decisions 0005, 0013–0016; kg-commons 0022, 0029, 0032).

1. Groups, computed fresh in every run, separately for series and events, by the identity links that join (declared
   in the catalogue and not below the quality threshold, kg-commons 0032) and by our linksets:
   - series: the series clusters of the event linksets (events.py: Springer and dblp by ls-springer-lod-dblp, the
     portal, ConfIDent and Wikidata by their dblp keys and Wikidata items, dblp by owl:sameAs), and the GND series by
     their Wikidata items (gnd owl:sameAs, wikidata wdt:P227);
   - events: the event linksets (ls-*-events), the dblp event IDs of Wikidata (wdt:P10692), the GND numbers of
     Springer conferences and Wikidata events (spr:hasGNDID, wdt:P227), the Wikidata items of the GND (owl:sameAs);
     the numbered parts of one dblp event are one event (events.py).
   A link joins only records of the same level (series, event); a link between levels joins nothing (it is counted).
   The records: Springer conference series and conferences, series and events of the portal, of ConfIDent, of
   Wikidata (series: wdt:P31 academic conference series or a dblp venue ID; events: events.py), the dblp venues of
   conferences and the dblp events, the GND series and events. The GND is authority data: its records join a group
   but never make one on their own.
2. Identifiers (decision 0005): a type letter (s, e), the number in lowercase Crockford base32, a Luhn mod 32 check
   character. Comparison with the previous version (its members): a group whose records belong to one old identifier
   keeps it; with records of several old identifiers, the oldest (lowest number) is kept and the others are merged
   into it (cr:mergedInto, cr:mergeDate); an old identifier whose records are now in several groups is split
   (cr:splitInto, cr:splitDate) and every part gets a new identifier; an old identifier with no record left is
   retired (cr:retiredDate). New groups get numbers from one counter, above the highest number ever issued (32**4 in
   the first version), in the order of their smallest record IRI. No number is used twice.
3. Facts, from the records in the precedence of the datasets (FACTS_ORDER): names and acronyms, the start date and
   the end date (if it is not before the start and at most 60 days after it), the place (schema:location: the Wikidata
   item of ls-places, a city before a region before a country, decision 0018; else the name as the source gives it),
   the edition number (cr:edition where the event has one series), the series of an event (cr:inSeries), the status
   and attendance mode (ConfIDent, decision 0016), the website (schema:url, ConfIDent and Wikidata), the proceedings
   (cr:proceedings: the volumes of dblp, Springer and Wikidata that name the event), and the academic fields and
   disciplines (cr:field, cr:discipline, ls-fields, decision 0019): an event without its own takes those of its
   series; a series has its own and those of at least FIELD_SHARE of its events.

Files: ids.ttl.gz (the series and events: class, cr:sameAs to every record, facts), ids-history.ttl.gz (merges,
splits, retirements; the history of the previous version is carried over), ids-members.tsv.gz (identifier, record,
source, dataset). The date of the events of the history is the date of the run (data, not a version id).
"""

import gzip
import io
import re
import urllib.parse
from collections import Counter, defaultdict
from datetime import date as date_of_iso, timedelta

from cr import catalog, identifiers, project
from cr.generator import GeneratorError, load_shared
from cr.rdf import IRI, RDF_TYPE, XSD, Literal

events = load_shared("ls-springer-lod-events", "events")

_E = catalog.Catalog().entries
INPUTS = {**events.INPUTS, "gnd": "gnd/2026-11-08",
          **{f"ls_{s.replace('-', '_')}_events": f"ls-{s}-events/2026-11-09"
             for s in ("springer-lod", "confref-portal", "confident", "wikidata")}}
INPUTS |= {"ls_places": "ls-places/2026-11-09", "wikidata_places": "wikidata-places/2026-11-09",
           "ls_fields": "ls-fields/2026-11-09"}
if "ids" in _E and _E["ids"].stable:
    INPUTS["previous"] = f"ids/{_E['ids'].stable}/ids-members.tsv.gz"
    INPUTS["previous_history"] = f"ids/{_E['ids'].stable}/ids-history.ttl.gz"
PARAMS = {}

BASE = project.BASE
CR = project.ONTOLOGY
SCHEMA = "http://schema.org/"
RDFS_LABEL = "http://www.w3.org/2000/01/rdf-schema#label"
W, WD = events.W, events.WD
GNDO = "https://d-nb.info/standards/elementset/gnd#"
SPR, PORTAL, CF, DBLP = events.SPR, events.PORTAL, events.CF, events.DBLP
SAME = "http://www.w3.org/2002/07/owl#sameAs"
REPLACED = "http://purl.org/dc/terms/isReplacedBy"

# precedence of the datasets for the facts: curated and current first, then the publishers and bibliographies, the
# knowledge base, the legacy portal, the authority file
FACTS_ORDER = ["confident", "springer", "dblp-venue", "dblp-event", "wikidata", "confref-portal", "gnd"]
AUTHORITY_ONLY = {"gnd"}
SOURCE_DATASET = {"springer": "springer-lod", "confref-portal": "confref-portal", "confident": "confident",
                  "wikidata": "wikidata", "dblp-venue": "dblp", "dblp-event": "dblp", "gnd": "gnd"}
STATUS = {"postponed": SCHEMA + "EventPostponed", "canceled": SCHEMA + "EventCancelled",
          "as scheduled": SCHEMA + "EventScheduled"}
MODE = {"on site": SCHEMA + "OfflineEventAttendanceMode", "online": SCHEMA + "OnlineEventAttendanceMode",
        "hybrid": SCHEMA + "MixedEventAttendanceMode"}
WD_SERIES = {WD + "Q47258130"}
FIELD_SHARE = 0.3   # a field of at least this share of the events of a series is a field of the series

# --- the form of an identifier (decision 0005) -------------------------------------------------------------------
ALPHABET = "0123456789abcdefghjkmnpqrstvwxyz"
FIRST = 32 ** 4
TYPES = {"series": "s", "event": "e"}
PATHS = {"s": "series/", "e": "event/"}


def check_char(digits):
    """Luhn mod 32 over the alphabet: the check character of a string of base32 digits."""
    total, factor = 0, 2
    for ch in reversed(digits):
        a = factor * ALPHABET.index(ch)
        total += a // 32 + a % 32
        factor = 1 if factor == 2 else 2
    return ALPHABET[(32 - total % 32) % 32]


def format_id(kind, number):
    digits = ""
    while number:
        digits, number = ALPHABET[number % 32] + digits, number // 32
    return TYPES[kind] + digits + check_char(digits)


def parse_id(ident):
    """(kind letter, number) of an identifier; ValueError if the form or the check character is wrong."""
    m = re.fullmatch(r"([se])([0-9a-hjkmnp-tv-z]+)([0-9a-hjkmnp-tv-z])", ident)
    if not m or check_char(m.group(2)) != m.group(3):
        raise ValueError(f"not a confref identifier: {ident}")
    n = 0
    for ch in m.group(2):
        n = n * 32 + ALPHABET.index(ch)
    return m.group(1), n


def iri_of(ident):
    return BASE + PATHS[ident[0]] + ident


# --- reading -----------------------------------------------------------------------------------------------------

def val(o):
    return o.value if isinstance(o, Literal) else str(o)


class Record:
    __slots__ = ("node", "iri", "level", "names", "acronyms", "facts")

    def __init__(self, node, iri, level):
        self.node, self.iri, self.level = node, iri, level
        self.names, self.acronyms, self.facts = [], [], {}


def level_of_node(node):
    src, ident = node
    if src in ("springer",):
        return "series" if ident.startswith("confseries/") else "event"
    if src == "confref-portal":
        return "series" if ident.startswith("series/") else "event"
    if src in ("dblp-venue", "wikicfp-series"):
        return "series"
    if src in ("dblp-event", "wikicfp-event"):
        return "event"
    return None   # confident, wikidata, gnd: from the class of the record


def read(run):
    uf, evs = events.read(run)
    records = {}
    level = {}

    def record(node, iri, lev):
        if node not in records:
            records[node] = Record(node, iri, lev)
            level[node] = lev
        return records[node]

    # events (with their facts and series) from events.py; the other parts of a dblp event
    part_of = {}
    for x, e in evs.items():
        r = record(x, e.iri, "event")
        r.facts.update({k: v for k, v in e.facts().items() if v})
        r.facts["series"] = set(e.series)
        if e.name:
            r.names.append(e.name)
        if e.acronym and e.source != "dblp-event":
            r.acronyms.append(e.acronym)
        if e.source == "dblp-event":
            r.facts["parts"] = sorted(e.extra)
            for part in e.extra:
                y = identifiers.identify(part)
                if y:
                    part_of[y] = x
    # series records and their names; GND; ConfIDent status and mode; Wikidata series
    for s, p, o in run.triples("springer"):
        if p == SPR + "confSeriesName":
            x = identifiers.identify(s)
            if x:
                record(x, str(s), "series").names.append(val(o))
    for s, p, o in run.triples("portal"):
        if "/confref-portal/series/" in str(s) and p in (PORTAL + "name", PORTAL + "acronym"):
            r = record(identifiers.identify(s), str(s), "series")
            (r.names if p == PORTAL + "name" else r.acronyms).append(val(o))
    cf_class, cf_vals = {}, defaultdict(list)
    for s, p, o in run.triples("confident"):
        if p == RDF_TYPE:
            cf_class[str(s)] = str(o)
        elif p in (CF + "Title", CF + "Acronym", CF + "Event_Status", CF + "Event_Mode"):
            cf_vals[str(s)].append((p[len(CF):], val(o)))
    for s, cls in cf_class.items():
        if cls == CF + "Category_Event_Series":
            r = record(identifiers.identify(s), s, "series")
        elif cls == CF + "Category_Event":
            r = records.get(identifiers.identify(s)) or record(identifiers.identify(s), s, "event")
        else:
            continue
        for k, v in cf_vals.get(s, []):
            if k == "Title" and r.level == "series":
                r.names.append(v)
            elif k == "Acronym" and r.level == "series":
                r.acronyms.append(v)
            elif k == "Event_Status" and v in STATUS:
                r.facts["status"] = STATUS[v]
            elif k == "Event_Mode" and v in MODE:
                r.facts["mode"] = MODE[v]
    wd = defaultdict(lambda: defaultdict(list))
    for s, p, o in run.triples("wikidata"):
        if p in (W + "P31", W + "P8926", W + "P1813", W + "P227", W + "P10692", W + "P179") or \
                (p == RDFS_LABEL and isinstance(o, Literal) and o.lang in ("en", "mul")):
            wd[str(s)][p].append(o)
    named_series = {str(o) for f in wd.values() for o in f.get(W + "P179", [])}
    for s, f in wd.items():
        x = identifiers.identify(s)
        if x in records:
            continue
        if set(map(str, f.get(W + "P31", []))) & WD_SERIES or f.get(W + "P8926") or s in named_series:
            r = record(x, s, "series")
            r.names += [val(o) for o in f.get(RDFS_LABEL, [])][:1]
            r.acronyms += [val(o) for o in f.get(W + "P1813", [])][:1]
    for s, p, o in run.triples("dblp"):
        if p in (DBLP + "streamTitle", DBLP + "primaryStreamTitle"):
            x = identifiers.identify(s)
            if x and x[0] == "dblp-venue" and x[1].startswith("conf/"):
                record(x, str(s), "series").names.append(val(o))
    gnd_class, gnd_name = {}, {}
    for s, p, o in run.triples("gnd"):
        if p == RDF_TYPE:
            gnd_class[str(s)] = str(o)
        elif p == GNDO + "preferredNameForTheConferenceOrEvent":
            gnd_name[str(s)] = val(o)
    for s, cls in gnd_class.items():
        lev = {GNDO + "SeriesOfConferenceOrEvent": "series", GNDO + "ConferenceOrEvent": "event"}.get(cls)
        if lev:
            r = record(identifiers.identify(s), s, lev)
            if s in gnd_name:
                r.names.append(gnd_name[s])
    return uf, records, part_of, wd


class Groups:
    """Union-find over the records of one level; a link to a record of another level joins nothing."""

    def __init__(self, lev, records):
        self.lev, self.records, self.parent = lev, records, {}
        self.across = Counter()

    def find(self, x):
        self.parent.setdefault(x, x)
        while self.parent[x] != x:
            self.parent[x] = self.parent[self.parent[x]]
            x = self.parent[x]
        return x

    def add(self, x):
        if x in self.records and self.records[x].level == self.lev:
            self.find(x)

    def union(self, a, b, why):
        la = self.records[a].level if a in self.records else level_of_node(a)
        lb = self.records[b].level if b in self.records else level_of_node(b)
        if (la and la != self.lev) or (lb and lb != self.lev):
            self.across[why] += 1
            return
        self.parent[self.find(a)] = self.find(b)

    def groups(self):
        out = defaultdict(set)
        for x in list(self.parent):
            out[self.find(x)].add(x)
        return [frozenset(m) for m in out.values()]


def group(run):
    uf, records, part_of, wd = read(run)
    series, evs = Groups("series", records), Groups("event", records)
    for x, r in records.items():
        (series if r.level == "series" else evs).add(x)
    # series: the clusters of events.py, the GND series by their Wikidata items
    for x in list(uf.parent):
        root = uf.find(x)
        if root != x:
            series.union(x, root, "series cluster")
    joins = identifiers.joins
    for s, p, o in run.triples("gnd"):
        if p == SAME and joins("gnd", p, "wikidata"):
            a, b = identifiers.identify(s), identifiers.identify(o)
            if a and b and b[0] == "wikidata":
                g = series if records.get(a) and records[a].level == "series" else evs
                g.union(a, b, "gnd owl:sameAs")
        elif p == REPLACED:
            a, b = identifiers.identify(s), identifiers.identify(o)
            if a in records and b:
                (series if records[a].level == "series" else evs).union(a, b, "gnd replaced")
    for s, f in wd.items():
        a = identifiers.identify(s)
        if a not in records:
            continue
        g = series if records[a].level == "series" else evs
        for o in f.get(W + "P227", []):
            b = identifiers.identify(o, W + "P227")
            if b and joins("wikidata", W + "P227", "gnd"):
                g.union(a, b, "wikidata P227")
        for o in f.get(W + "P10692", []):
            b = identifiers.identify(o, W + "P10692")
            if b and joins("wikidata", W + "P10692", "dblp-event"):
                evs.union(a, part_of.get(b, b), "wikidata P10692")
    for s, p, o in run.triples("springer"):
        if p == SPR + "hasGNDID" and joins("springer-lod", p, "gnd"):
            a, b = identifiers.identify(s), identifiers.identify(o)
            if a and b:
                evs.union(a, b, "springer hasGNDID")
    for name in ("ls_springer_lod_events", "ls_confref_portal_events", "ls_confident_events", "ls_wikidata_events"):
        slug = INPUTS[name].split("/")[0]
        for s, p, o in run.triples(name):
            a, b = identifiers.identify(s), identifiers.identify(o, p)
            if a and b and joins(slug, p, b[0]):
                evs.union(a, part_of.get(b, b), slug)
    out = []
    for lev, g in (("series", series), ("event", evs)):
        for members in g.groups():
            recs = [records[m] for m in members if m in records and records[m].level == lev]
            if recs and not all(r.node[0] in AUTHORITY_ONLY for r in recs):
                out.append((lev, recs))
    return out, records, series.across + evs.across


# --- facts -------------------------------------------------------------------------------------------------------

def rank(r):
    return (FACTS_ORDER.index(r.node[0]) if r.node[0] in FACTS_ORDER else len(FACTS_ORDER), r.iri)


def first(recs, key):
    for r in sorted(recs, key=rank):
        v = r.facts.get(key)
        if v:
            return v
    return None


def names(recs):
    seen, out = set(), []
    for r in sorted(recs, key=rank):
        for n in r.names:
            if n and n.lower() not in seen:
                seen.add(n.lower())
                out.append(n)
    return out


def acronyms(recs):
    seen, out = set(), []
    for r in sorted(recs, key=rank):
        for a in r.acronyms:
            k = events.norm_acronym(a)
            if k and k not in seen:
                seen.add(k)
                out.append(a)
    return out


def read_more(run, records):
    """The facts of the records that events.py does not read (version 2): end dates, websites, proceedings, places
    (ls-places, with their level from wikidata-places), fields and disciplines (ls-fields). Sets them in r.facts."""
    by_iri = {r.iri: r for r in records.values()}
    for r in list(records.values()):
        for other in r.facts.get("parts", ()):
            by_iri.setdefault(other, r)

    def put(iri, key, value, many=False):
        r = by_iri.get(str(iri))
        if r is None or value in (None, ""):
            return
        if many:
            r.facts.setdefault(key, set()).add(value)
        else:
            r.facts.setdefault(key, value)

    for s, p, o in run.triples("springer"):
        if p == SPR + "confEndDate":
            put(s, "end", events.day_of(val(o)))
        elif p == SPR + "proceedingsOf":
            put(o, "proceedings", str(s), True)
    for s, p, o in run.triples("portal"):
        if p == PORTAL + "endDate":
            put(s, "end", events.day_of(val(o)))
    for s, p, o in run.triples("confident"):
        if p == CF + "End_Date":
            put(s, "end", events.day_of(val(o)))
        elif p == CF + "Official_Website" and val(o).startswith("http"):
            put(s, "url", val(o))
    for s, p, o in run.triples("wikidata"):
        if p == W + "P582":
            put(s, "end", events.day_of(val(o)))
        elif p == W + "P856":
            put(s, "url", str(o))
        elif p == W + "P4745":
            put(o, "proceedings", str(s), True)
    toc_of = defaultdict(list)
    for s, p, o in run.triples("dblp"):
        if p == DBLP + "listedOnTocPage":
            put(o, "proceedings", str(s), True)
    # places: the level of each place
    level = {}
    for s, p, o in run.triples("wikidata_places"):
        if p == W + "P297":
            level[str(s)] = 3
        elif p == W + "P300":
            level.setdefault(str(s), 2)
        elif p == W + "P625":
            level.setdefault(str(s), 1)
    for s, p, o in run.triples("ls_places"):
        r = by_iri.get(str(s))
        if r is not None:
            r.facts.setdefault("places", set()).add((level.get(str(o), 4), str(o)))
    disc_field = defaultdict(set)
    for s, p, o in run.triples("ls_fields"):
        if p == CR + "field" and str(s) not in by_iri:
            disc_field[str(s)].add(str(o))
            continue
        r = by_iri.get(str(s))
        if r is not None:
            r.facts.setdefault("fields" if p == CR + "field" else "disciplines", set()).add(str(o))
    for r in records.values():
        if r.facts.get("end"):
            r.facts["end"] = r.facts["end"].isoformat()
    return disc_field


def date_of(iso):
    return date_of_iso.fromisoformat(iso)


def place_of(recs):
    """The most specific place of the record first in precedence that has one (city before region before country)."""
    best = None
    for r in sorted(recs, key=rank):
        for lev, item in sorted(r.facts.get("places", ())):
            if best is None or lev < best[0]:
                best = (lev, item)
        if best and best[0] == 1:
            break
    return best[1] if best else None


def union(recs, key):
    return set().union(*(r.facts.get(key, set()) for r in recs))


# --- identifiers and history -------------------------------------------------------------------------------------

def read_previous(run):
    """({identifier: {member IRI}}, highest number ever issued, history triples)."""
    if "previous" not in INPUTS:
        return {}, FIRST - 1, []
    members, history, high = defaultdict(set), [], FIRST - 1
    for f in run.inputs("previous"):
        if f.name == "ids-members.tsv.gz":
            with gzip.open(f, "rt", encoding="utf-8") as g:
                next(g)
                for line in g:
                    ident, iri = line.rstrip("\n").split("\t")[:2]
                    members[ident].add(iri)
                    high = max(high, parse_id(ident)[1])
    for s, p, o in run.triples("previous_history"):
        history.append((s, p, o))
        for t in (s, o):
            if isinstance(t, str) and t.startswith(BASE) and "/" in t[len(BASE):]:
                high = max(high, parse_id(t.rsplit("/", 1)[1])[1])
    return members, high, history


def generate(run):
    groups, records, across = group(run)
    read_more(run, records)
    run.log(f"groups: {Counter(lev for lev, _ in groups)}; links between levels (not joined): {dict(across)}")
    prev, high, history = read_previous(run)
    old_of = {iri: ident for ident, iris in prev.items() for iri in iris}
    d = run.id[4:12]   # the date of the run: the date of the events of the history
    date = Literal(f"{d[:4]}-{d[4:6]}-{d[6:]}", XSD + "date", None)
    # old identifiers per group, groups per old identifier
    olds = [sorted({old_of[r.iri] for r in recs if r.iri in old_of}, key=lambda i: parse_id(i)[1]) for _, recs in groups]
    parts = defaultdict(set)
    for i, os_ in enumerate(olds):
        for o in os_:
            parts[o].add(i)
    hist = set(history)
    assigned = {}
    split_ids = {o for o, gs in parts.items() if len(gs) > 1}
    for i, os_ in enumerate(olds):
        keep = [o for o in os_ if o not in split_ids]
        if keep:
            assigned[i] = keep[0]
            for o in keep[1:]:
                hist |= {(IRI(iri_of(o)), IRI(CR + "mergedInto"), IRI(iri_of(keep[0]))),
                         (IRI(iri_of(o)), IRI(CR + "mergeDate"), date)}
    new = sorted((i for i in range(len(groups)) if i not in assigned), key=lambda i: min(r.iri for r in groups[i][1]))
    for i in new:
        high += 1
        assigned[i] = format_id(groups[i][0], high)
    for o in split_ids:
        for i in parts[o]:
            hist.add((IRI(iri_of(o)), IRI(CR + "splitInto"), IRI(iri_of(assigned[i]))))
        hist.add((IRI(iri_of(o)), IRI(CR + "splitDate"), date))
    present = set(assigned.values())
    for o in prev:
        if o not in present and o not in parts:
            hist |= {(IRI(iri_of(o)), IRI(CR + "retiredDate"), date)}
    if len(present) != len(groups):
        raise GeneratorError("two groups got the same identifier")
    # the series identifier of every series record, for cr:inSeries
    series_id = {r.node: assigned[i] for i, (lev, recs) in enumerate(groups) if lev == "series" for r in recs}
    # fields and disciplines: an event without its own takes those of its series; a series takes those of its own
    # records and those of at least FIELD_SHARE of its events
    own = {i: (union(recs, "fields"), union(recs, "disciplines")) for i, (lev, recs) in enumerate(groups)}
    series_index = {assigned[i]: i for i, (lev, _r) in enumerate(groups) if lev == "series"}
    ev_series = {}
    for i, (lev, recs) in enumerate(groups):
        if lev == "event":
            ev_series[i] = sorted({series_id[n] for r in recs for n in r.facts.get("series", ()) if n in series_id})
    counts = defaultdict(lambda: (Counter(), Counter(), [0]))
    for i, sids in ev_series.items():
        for sid in sids:
            f, d, n = counts[series_index[sid]]
            f.update(own[i][0])
            d.update(own[i][1])
            n[0] += 1
    fields_of, disciplines_of = {}, {}
    for i, (lev, recs) in enumerate(groups):
        if lev == "series":
            f, d, n = counts[i]
            fields_of[i] = own[i][0] | {k for k, v in f.items() if n[0] and v >= FIELD_SHARE * n[0]}
            disciplines_of[i] = own[i][1] | {k for k, v in d.items() if n[0] and v >= FIELD_SHARE * n[0]}
    for i, sids in ev_series.items():
        fields_of[i] = own[i][0] or set().union(*(own[series_index[s]][0] for s in sids)) if sids else own[i][0]
        disciplines_of[i] = own[i][1] or (set().union(*(own[series_index[s]][1] for s in sids)) if sids else set())
    triples, rows = set(), ["id\trecord\tsource\tdataset"]
    for i, (lev, recs) in enumerate(groups):
        ident = assigned[i]
        x = IRI(iri_of(ident))
        triples.add((x, IRI(RDF_TYPE), IRI(CR + ("Series" if lev == "series" else "Event"))))
        for r in sorted(recs, key=rank):
            triples.add((x, IRI(CR + "sameAs"), IRI(r.iri)))
            rows.append(f"{ident}\t{r.iri}\t{r.node[0]}\t{SOURCE_DATASET.get(r.node[0], '')}")
            if r.node[0] == "dblp-event":
                for other in r.facts.get("parts", ()):
                    triples.add((x, IRI(CR + "sameAs"), IRI(other)))
                    rows.append(f"{ident}\t{other}\tdblp-event\tdblp")
        ns = names(recs)
        if ns:
            triples.add((x, IRI(RDFS_LABEL), Literal(ns[0], None, None)))
            triples.add((x, IRI(SCHEMA + "name"), Literal(ns[0], None, None)))
        for a in acronyms(recs)[:3]:
            triples.add((x, IRI(SCHEMA + "alternateName"), Literal(a, None, None)))
        if lev == "event":
            start = first(recs, "start")
            if start:
                triples.add((x, IRI(SCHEMA + "startDate"), Literal(start, XSD + "date", None)))
                end = first(recs, "end")
                if end and end >= start and end <= (date_of(start) + timedelta(days=60)).isoformat():
                    triples.add((x, IRI(SCHEMA + "endDate"), Literal(end, XSD + "date", None)))
            place = place_of(recs)
            if place:
                triples.add((x, IRI(SCHEMA + "location"), IRI(place)))
            else:
                place = first(recs, "place")
                if place and not re.fullmatch(r"Q[0-9]+", place):
                    triples.add((x, IRI(SCHEMA + "location"), Literal(place, None, None)))
            for p in sorted(union(recs, "proceedings")):
                triples.add((x, IRI(CR + "proceedings"), IRI(p)))
            sids = sorted({series_id[n] for r in recs for n in r.facts.get("series", ()) if n in series_id})
            for sid in sids:
                triples.add((x, IRI(CR + "inSeries"), IRI(iri_of(sid))))
            number = first(recs, "number")
            if number and len(sids) == 1:
                triples.add((x, IRI(CR + "edition"), Literal(str(number), XSD + "integer", None)))
            for key, prop in (("status", "eventStatus"), ("mode", "eventAttendanceMode")):
                v = first(recs, key)
                if v:
                    triples.add((x, IRI(SCHEMA + prop), IRI(v)))
        url = first(recs, "url")
        if url:
            url = urllib.parse.quote(url.strip(), safe=":/?#[]@!$&'()*+,;=%~")
            if re.fullmatch(r"https?://[^\s<>\"{}\\^`]+", url):
                triples.add((x, IRI(SCHEMA + "url"), IRI(url)))
        for f in sorted(fields_of.get(i, ())):
            triples.add((x, IRI(CR + "field"), IRI(f)))
        for d in sorted(disciplines_of.get(i, ())):
            triples.add((x, IRI(CR + "discipline"), IRI(d)))
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as f:
        f.write(("\n".join(rows[:1] + sorted(rows[1:])) + "\n").encode("utf-8"))
    run.path("ids-members.tsv.gz").write_bytes(buf.getvalue())
    run.write_turtle("ids.ttl.gz", triples)
    run.write_turtle("ids-history.ttl.gz", hist)
    c = Counter(lev for lev, _ in groups)
    run.note(f"{c['series']:,} series and {c['event']:,} events; {len(new):,} new identifiers (up to number {high:,}); "
             f"{len(prev):,} in the previous version; history: {len(hist):,} statements.")

