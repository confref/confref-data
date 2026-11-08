"""confident: ConfIDent (TIB), the registry of academic events, true to the source (decision 0011).

Source: a harvest of the ConfIDent API (harvest.py; inputs:confident/<date>): the semantic data of every page of the
categories Event, Event Series, Organization, Academic Field and Country and of the subobjects Organizer, Deadline and
Maintainer (SMW Ask API), the page IDs, and the deletions, moves and merges of the five namespaces. CC0 (page footer,
Terms of Use).

Records: data/confident/<page ID> for a page (the page ID survives moves, the title does not; ConfIDent's own RDF IRIs
are malformed), data/confident/<page ID>/<subobject id> for a subobject, data/confident/log/<log ID> for an event of
the log. Every record: rdf:type its category (vocab/Category_Event, …), rdfs:label (the display title), vocab:pageTitle and
vocab:page (its page on confident-conference.org); subobjects are linked from their page by vocab:Has_subobject, as
in SMW.

Properties: one per SMW property, named by the property (vocab/<Property_name>; the built-in properties by their label,
e.g. vocab/Modification_date; described with its name, the label
ConfIDent shows and its type in confident-vocabulary.ttl.gz), values by the SMW type: dates as xsd:date (xsd:gYear,
xsd:gYearMonth, xsd:dateTime by the precision given), numbers as xsd:integer or xsd:decimal, booleans as xsd:boolean,
URLs as IRIs (xsd:anyURI literals where not a valid IRI), references to pages as the IRI of that page's record (a
literal with the title where the page does not exist), text and identifiers (DOI, DBLP, Wikidata, ROR, …) as given.

Left out: Title_Search and Semantic_Dependency (helpers of the wiki: the title in lower case, the page itself) and
Meeting_URL (links to online meetings, often with their password). The calendar subobjects (Color, Title, _dat) are not
harvested. The log has no user names and no comments (comments of deletions repeat the deleted text).
"""

import json
import re
from collections import Counter
from urllib.parse import quote

from cr import project
from cr.rdf import IRI, RDF_TYPE, XSD, Literal

INPUTS = {"harvest": "inputs:confident/2026-11-08"}
PARAMS = {}

NS = project.DATA + "confident/"
V = NS + "vocab/"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
RDFP = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
SITE = "https://www.confident-conference.org/index.php/"
SMW_TYPE = "http://semantic-mediawiki.org/swivt/1.0#"
LEFT_OUT = {"Title_Search", "Semantic_Dependency", "Meeting_URL"}
PAGE_CATEGORIES = ["Event", "Event_Series", "Organization", "Academic_Field", "Country"]
SUBOBJECT_CATEGORIES = ["Organizer", "Deadline", "Maintainer"]
_BAD_IRI = re.compile(r'[\x00-\x20<>"{}|^`\\]')


def by_folder(run, folder):
    return sorted((p for p in run.inputs("harvest") if p.suffix == ".json" and p.parent.name == folder
                   and p.parent.parent.name in ("ask", "pages", "log")), key=lambda p: p.name)


def page_iri(pageid):
    return IRI(NS + str(pageid))


def page_url(title):
    return IRI(SITE + quote(title.replace(" ", "_"), safe="/:_-.,()!'*~"))


def date_value(v):
    """An SMW date ("1/2026/9/30", calendar model first) as a typed literal by its precision."""
    parts = v["raw"].split("/")
    if parts[0] != "1":   # not the Gregorian calendar: as given
        return Literal(v["raw"], None, None)
    y, rest = parts[1], [int(x) for x in parts[2:]]
    year = y if y.startswith("-") else y.zfill(4)
    if not rest:
        return Literal(year, XSD + "gYear", None)
    if len(rest) == 1:
        return Literal(f"{year}-{rest[0]:02d}", XSD + "gYearMonth", None)
    if len(rest) == 2:
        return Literal(f"{year}-{rest[0]:02d}-{rest[1]:02d}", XSD + "date", None)
    h, m, s = (rest[2:] + [0, 0, 0])[:3]
    return Literal(f"{year}-{rest[0]:02d}-{rest[1]:02d}T{h:02d}:{m:02d}:{s:02d}", XSD + "dateTime", None)


class Converter:
    def __init__(self, run, pageids):
        self.run, self.pageids = run, pageids
        self.properties = {}   # key -> (label, typeid)
        self.missing_pages = Counter()

    def value(self, typeid, v):
        if typeid == "_dat":
            return date_value(v)
        if typeid == "_wpg":
            pid = self.pageids.get(v["fulltext"])
            if pid is None:
                self.missing_pages[v["fulltext"].split(":")[0]] += 1
                return Literal(v["fulltext"], None, None)
            return page_iri(pid)
        if typeid == "_num":
            return Literal(str(v), XSD + ("integer" if isinstance(v, int) else "decimal"), None)
        if typeid == "_boo":
            return Literal("true" if v in ("t", True, "true", "1") else "false", XSD + "boolean", None)
        if typeid == "_uri":
            return IRI(v) if not _BAD_IRI.search(v) and re.match(r"^[a-z][a-z0-9+.-]*:", v, re.I) else \
                Literal(v, XSD + "anyURI", None)
        return Literal(str(v), None, None)

    def records(self, folder, cls, subobjects=False):
        """The triples of the results of one Ask query (all its files)."""
        n = 0
        for f in by_folder(self.run, folder):
            data = json.loads(f.read_bytes())
            requests = {pr["label"]: (pr["key"], pr["typeid"]) for pr in data["query"]["printrequests"] if pr["label"]}
            for title, r in (data["query"]["results"] or {}).items():
                n += 1
                if subobjects:
                    page, _, sub = title.partition("#")
                    pid = self.pageids.get(page)
                    if pid is None:
                        self.missing_pages["subobject of a missing page"] += 1
                        continue
                    s = IRI(f"{page_iri(pid)}/{quote(sub.strip(), safe='')}")
                else:
                    pid = self.pageids.get(title)
                    if pid is None:
                        self.missing_pages["result without page ID"] += 1
                        continue
                    s = page_iri(pid)
                    yield s, IRI(RDFS + "label"), Literal(r.get("displaytitle") or title.split(":", 1)[1], None, None)
                    yield s, IRI(V + "pageTitle"), Literal(title, None, None)
                    yield s, IRI(V + "page"), page_url(title)
                yield s, IRI(RDF_TYPE), IRI(V + "Category_" + cls)
                for label, vals in r["printouts"].items():
                    key, typeid = requests[label]
                    if label == "Page" and subobjects:   # ?-Has subobject: the page this subobject belongs to
                        for v in vals:
                            ppid = self.pageids.get(v["fulltext"])
                            if ppid is not None:
                                yield page_iri(ppid), IRI(V + "Has_subobject"), s
                        continue
                    # SMW's built-in properties have internal keys (_MDAT, _CDAT, _DTITLE): named by their label
                    key = label.replace(" ", "_") if key.startswith("_") else key
                    if key in LEFT_OUT:
                        continue
                    self.properties.setdefault(key, (label, typeid))
                    for v in vals:
                        yield s, IRI(V + key), self.value(typeid, v)
        self.run.log(f"{folder}: {n:,} results")


def pageids(run):
    ids = {}
    for f in run.inputs("harvest"):
        if f.suffix == ".json" and f.parent.parent.name == "pages":
            for p in json.loads(f.read_bytes())["query"]["allpages"]:
                ids[p["title"]] = p["pageid"]
    return ids


def log_events(run, ids):
    for f in sorted(run.inputs("harvest")):
        if f.suffix != ".json" or f.parent.parent.name != "log":
            continue
        for e in json.loads(f.read_bytes())["query"]["logevents"]:
            s = IRI(NS + "log/" + str(e["logid"]))
            yield s, IRI(RDF_TYPE), IRI(V + "LogEvent")
            yield s, IRI(V + "logType"), Literal(e["type"], None, None)
            yield s, IRI(V + "logAction"), Literal(e["action"], None, None)
            yield s, IRI(V + "logTitle"), Literal(e["title"], None, None)
            yield s, IRI(V + "logTimestamp"), Literal(e["timestamp"], XSD + "dateTime", None)
            if e.get("pageid") and e["pageid"] in ids.values():
                yield s, IRI(V + "logPage"), page_iri(e["pageid"])
            target = (e.get("params") or {}).get("target_title")
            if target:
                yield s, IRI(V + "logTarget"), Literal(target, None, None)
                if target in ids:
                    yield s, IRI(V + "logTargetPage"), page_iri(ids[target])


OWN_TERMS = [
    ("Category_Event", "class", "Event", "A page of the category Event."),
    ("Category_Event_Series", "class", "Event series", "A page of the category Event Series."),
    ("Category_Organization", "class", "Organization", "A page of the category Organization."),
    ("Category_Academic_Field", "class", "Academic field", "A page of the category Academic Field."),
    ("Category_Country", "class", "Country", "A page of the category Country."),
    ("Category_Organizer", "class", "Organizer", "A subobject of the category Organizer (an organizer of an event)."),
    ("Category_Deadline", "class", "Deadline", "A subobject of the category Deadline (a deadline of an event)."),
    ("Category_Maintainer", "class", "Maintainer", "A subobject of the category Maintainer (a maintainer of a series)."),
    ("LogEvent", "class", "Log event", "A deletion, move or merge of a page, from the log of the wiki."),
    ("pageTitle", "property", "page title", "The title of the page in the wiki."),
    ("page", "property", "page", "The page in the wiki."),
    ("Has_subobject", "property", "has subobject", "A subobject of the page (SMW: Has subobject)."),
    ("logType", "property", "log type", "delete, move or merge."),
    ("logAction", "property", "log action", "The action of the log event (e.g. delete, restore, move)."),
    ("logTitle", "property", "log title", "The title of the page the log event is about."),
    ("logTimestamp", "property", "log timestamp", "When the log event happened."),
    ("logPage", "property", "log page", "The record of the page the log event is about, where it still exists."),
    ("logTarget", "property", "move target", "The title a page was moved to."),
    ("logTargetPage", "property", "move target page", "The record of the page a page was moved to."),
]


def vocabulary(properties):
    def term(local, kind, label, comment):
        t = IRI(V + local)
        yield t, IRI(RDF_TYPE), IRI(RDFS + "Class" if kind == "class" else RDFP)
        yield t, IRI(RDFS + "label"), Literal(label, None, "en")
        yield t, IRI(RDFS + "comment"), Literal(comment, None, "en")
    for x in OWN_TERMS:
        yield from term(*x)
    for key, (label, typeid) in sorted(properties.items()):
        name = key.replace("_", " ")
        shown = f" (shown as \"{label}\")" if label != name else ""
        yield from term(key, "property", name, f"The SMW property {name} of ConfIDent{shown}, of type {typeid}.")
        yield IRI(V + key), IRI(RDFS + "seeAlso"), page_url("Property:" + name)


def generate(run):
    ids = pageids(run)
    run.log(f"{len(ids):,} page IDs")
    c = Converter(run, ids)

    def data():
        for cls in PAGE_CATEGORIES:
            yield from c.records(cls, cls)
        for cls in SUBOBJECT_CATEGORIES:
            yield from c.records(cls, cls, subobjects=True)

    run.write_turtle("confident.ttl.gz", data())
    for k, n in sorted(c.missing_pages.items()):
        run.log(f"  without page ID: {k}: {n:,}")
    run.write_turtle("confident-log.ttl.gz", log_events(run, ids))
    run.write_turtle("confident-vocabulary.ttl.gz", vocabulary(c.properties))
