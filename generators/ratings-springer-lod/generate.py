"""ratings-springer-lod: the ratings of conference series that Springer published in its LOD (decision 0020).

Source: the dataset springer-lod (lod.springer.com, 2018, CC0): on 742 conference series the ratings Springer
loaded on 2017-04-06 (spr:ratingLoadingDate): CORE (spr:ratingCORE), Qualis (spr:ratingQUALIS), GII-GRIN-SCIE
(spr:ratingGIIGRIN), CCF (spr:ratingCCF), each a Springer IRI http://lod.springer.com/data/confrating/<system>/<value>;
and the Google Scholar h5-index and h5-median (spr:googleScholarH5Index, spr:googleScholarH5Median, with the link of
the venue in Google Scholar, spr:googleScholarLink, of 2017).

Each rating is a cr:Rating, https://id.confref.org/data/ratings-springer-lod/<series key>/<system>: the series
(cr:ratingOf, Springer's IRI), the system (cr:ratingSystem, a concept of rating-systems), the value (cr:ratingValue,
as Springer gives it), the date Springer loaded it (dcterms:date) and, for Google Scholar, the page (dcterms:source).
Springer did not record which edition of a ranking it loaded; the date is the date of loading.
"""

from cr import project
from cr.generator import load_shared
from cr.rdf import IRI, RDF_TYPE, Literal

systems = load_shared("rating-systems", "generate")

INPUTS = {"springer": "springer-lod/2026-11-08"}
PARAMS = {}

SPR = "http://lod.springer.com/data/ontology/property/"
CR = project.ONTOLOGY
DCT = "http://purl.org/dc/terms/"
XSD = "http://www.w3.org/2001/XMLSchema#"
BASE = project.DATA + "ratings-springer-lod/"
RATINGS = {"ratingCORE": "core", "ratingQUALIS": "qualis", "ratingGIIGRIN": "gii-grin-scie", "ratingCCF": "ccf",
           "googleScholarH5Index": "h5-index", "googleScholarH5Median": "h5-median"}


def generate(run):
    facts = {}
    for s, p, o in run.triples("springer"):
        if p.startswith(SPR) and str(s).startswith("http://lod.springer.com/data/confseries/"):
            facts.setdefault(str(s), {}).setdefault(p[len(SPR):], o)
    t = set()
    count = {}
    for series, f in sorted(facts.items()):
        date = f.get("ratingLoadingDate")
        key = series.rsplit("/", 1)[1]
        for prop, system in RATINGS.items():
            if prop not in f:
                continue
            o = f[prop]
            value = o.value if isinstance(o, Literal) else str(o).rsplit("/", 1)[1]
            r = IRI(BASE + key + "/" + system)
            t.add((r, IRI(RDF_TYPE), IRI(CR + "Rating")))
            t.add((r, IRI(CR + "ratingOf"), IRI(series)))
            t.add((r, IRI(CR + "ratingSystem"), IRI(systems.iri(system))))
            if system.startswith("h5"):
                t.add((r, IRI(CR + "ratingValue"), Literal(value, XSD + "integer", None)))
                if "googleScholarLink" in f:
                    t.add((r, IRI(DCT + "source"), IRI(str(f["googleScholarLink"]))))
                t.add((r, IRI(DCT + "date"), Literal("2017", XSD + "gYear", None)))
            else:
                t.add((r, IRI(CR + "ratingValue"), Literal(value, None, None)))
                if date is not None:
                    t.add((r, IRI(DCT + "date"), Literal(date.value, XSD + "date", None)))
            count[system] = count.get(system, 0) + 1
    run.note("Ratings: " + ", ".join(f"{k} {v:,}" for k, v in sorted(count.items())) + ".")
    run.write_turtle("ratings-springer-lod.ttl.gz", t)
