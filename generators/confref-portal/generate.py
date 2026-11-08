"""confref-portal: the conferences of portal.confref.org as its API delivered them on 2020-07-11 (decision 0010).

Source: inputs:confref/portal-2020/confref.tgz, confref/confref-conferences.json: 37,945 conferences of 5,668 series,
downloaded by Wolfgang Fahl through http://portal.confref.org/api/conferences/ and kept by ConferenceCorpus (the
areas and countries files of the archive are HTML error pages and are not read).

True to the API: one resource per conference (data/confref-portal/event/<id>), per series
(data/confref-portal/series/<id>) and per research area (data/confref-portal/area/<id>), with a property per field of
the API, coined in the dataset namespace (data/confref-portal/vocab/; described in
confref-portal-vocabulary.ttl.gz). Fields that are null are left out; every other value is stated as given, also the
placeholders of the source (dates on 1 January, impossible years). Text: the HTML character references of the API
are decoded ("f&#252;r" is "für"), nothing else is changed. Dates (YYYY-MM-DD) as xsd:date, the year as xsd:integer,
the DBLP id as an IRI, keywords as one literal each. In addition: rdfs:label (the name; for areas the value) and the
page of the conference on the portal (vocab:portalPage, offline since 2022).
"""

import html
import json
import re
import tarfile
from urllib.parse import quote

from cr import project
from cr.rdf import IRI, RDF_TYPE, XSD, Literal

INPUTS = {"api": "inputs:confref/portal-2020/confref.tgz"}
PARAMS = {}

MEMBER = "confref/confref-conferences.json"
NS = project.DATA + "confref-portal/"
V = NS + "vocab/"
RDFS = "http://www.w3.org/2000/01/rdf-schema#"
RDFP = "http://www.w3.org/1999/02/22-rdf-syntax-ns#Property"
PAGE = "http://portal.confref.org/list/"
DATE = re.compile(r"^\d{4}-\d{2}-\d{2}$")

# the terms: (local name, kind, label, comment); properties named as the fields of the API
TERMS = [
    ("Conference", "class", "Conference", "A conference of portal.confref.org (an element of /api/conferences/)."),
    ("Series", "class", "Conference series", "The series of a conference (the field confSeries)."),
    ("Area", "class", "Research area", "A research area of the portal (the field area)."),
    ("name", "property", "name", "The name of the conference or of the series."),
    ("acronym", "property", "acronym", "The acronym of the conference."),
    ("country", "property", "country", "The country of the conference, as text."),
    ("city", "property", "city", "The city of the conference, as text."),
    ("year", "property", "year", "The year of the conference."),
    ("startDate", "property", "start date", "The first day of the conference; often a placeholder (1 January)."),
    ("endDate", "property", "end date", "The last day of the conference; often a placeholder (1 January)."),
    ("description", "property", "description", "A description of the conference or the series."),
    ("shortDescription", "property", "short description", "A short description of the conference."),
    ("address", "property", "address", "The address of the conference venue."),
    ("submissionDate", "property", "submission date", "The submission deadline."),
    ("notificationDate", "property", "notification date", "The notification date."),
    ("submissionExtended", "property", "submission extended", "Whether the submission deadline was extended."),
    ("cameraReadyDate", "property", "camera-ready date", "The camera-ready deadline."),
    ("series", "property", "series", "The series of the conference (the field confSeries)."),
    ("issn", "property", "ISSN", "The ISSN of the proceedings series."),
    ("eissn", "property", "eISSN", "The electronic ISSN of the proceedings series."),
    ("dblpId", "property", "DBLP id", "The DBLP page of the series, as the portal gave it, or the key of the venue (literal) where the portal gave only that."),
    ("area", "property", "research area", "The research area of the conference."),
    ("keyword", "property", "keyword", "A keyword of the conference (the field keywords, one value each)."),
    ("portalPage", "property", "page on the portal", "The page of the conference on portal.confref.org (offline)."),
]


def text(value):
    return Literal(html.unescape(value), None, None)


def iri(kind, ident):
    return IRI(NS + kind + "/" + quote(str(ident), safe="-._~"))


def value(field, v):
    if isinstance(v, bool):
        return Literal("true" if v else "false", XSD + "boolean", None)
    if isinstance(v, int):
        return Literal(str(v), XSD + "integer", None)
    if field.endswith("Date") and DATE.match(v):
        return Literal(v, XSD + "date", None)
    return text(v)


def records(items, log):
    series, areas = {}, {}
    for r in items:
        e = iri("event", r["id"])
        yield e, IRI(RDF_TYPE), IRI(V + "Conference")
        yield e, IRI(RDFS + "label"), text(r["name"])
        yield e, IRI(V + "portalPage"), IRI(PAGE + quote(r["id"], safe="-._~"))
        for field in ("name", "acronym", "country", "city", "year", "startDate", "endDate", "description",
                      "shortDescription", "address", "submissionDate", "notificationDate", "submissionExtended",
                      "cameraReadyDate"):
            if r.get(field) is not None:
                yield e, IRI(V + field), value(field, r[field])
        for k in r["keywords"]:
            yield e, IRI(V + "keyword"), text(k)
        if r["ranks"]:
            raise ValueError(f"{r['id']}: ranks are not mapped (always empty in 2020)")
        s = r["confSeries"]
        yield e, IRI(V + "series"), iri("series", s["id"])
        series[s["id"]] = s
        a = r["area"]
        if a and a.get("id") is not None:
            yield e, IRI(V + "area"), iri("area", a["id"])
            areas[a["id"]] = a["value"]
    log(f"{len(series):,} series, {len(areas):,} areas")
    for sid, s in sorted(series.items()):
        x = iri("series", sid)
        yield x, IRI(RDF_TYPE), IRI(V + "Series")
        if s.get("name"):
            yield x, IRI(RDFS + "label"), text(s["name"])
        for field in ("name", "issn", "eissn", "description"):
            if s.get(field):
                yield x, IRI(V + field), text(s[field])
        if s.get("dblpId"):   # a page of dblp, or (145 series) only the key of the venue: then a literal
            d = s["dblpId"].strip()
            yield x, IRI(V + "dblpId"), IRI(d) if re.match(r"^https?://", d) else Literal(d, None, None)
    for aid, label in sorted(areas.items()):
        x = iri("area", aid)
        yield x, IRI(RDF_TYPE), IRI(V + "Area")
        if label:
            yield x, IRI(RDFS + "label"), text(label)


def vocabulary():
    for local, kind, label, comment in TERMS:
        t = IRI(V + local)
        yield t, IRI(RDF_TYPE), IRI(RDFS + "Class" if kind == "class" else RDFP)
        yield t, IRI(RDFS + "label"), Literal(label, None, "en")
        yield t, IRI(RDFS + "comment"), Literal(comment, None, "en")


def generate(run):
    with tarfile.open(run.input("api"), "r:gz") as t:
        items = json.load(t.extractfile(MEMBER))
    run.log(f"{len(items):,} conferences in {MEMBER}")
    run.write_turtle("confref-portal.ttl.gz", records(items, run.log))
    run.write_turtle("confref-portal-vocabulary.ttl.gz", vocabulary())
