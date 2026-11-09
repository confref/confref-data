"""rating-systems: the rating systems that the rating datasets use, as SKOS concepts (decision 0020).

Each system is https://id.confref.org/data/rating-systems/<name>: its name, who publishes it, its homepage and its
scale. The systems are described, not their ratings: those are in the rating datasets, each with its source and date.
"""

from cr import project
from cr.rdf import IRI, RDF_TYPE, Literal

INPUTS = {}
PARAMS = {}

SKOS = "http://www.w3.org/2004/02/skos/core#"
DCT = "http://purl.org/dc/terms/"
FOAF = "http://xmlns.com/foaf/0.1/"
BASE = project.DATA + "rating-systems"

SYSTEMS = [
    ("core", "CORE Conference Ranking", "CORE (Computing Research and Education Association of Australasia), now ICORE",
     "https://portal.core.edu.au/conf-ranks/", "A*, A, B, C (and Australasian, National, Unranked)",
     "A ranking of computer science conferences by a committee of the association, revised every few years."),
    ("qualis", "Qualis", "CAPES (Coordenação de Aperfeiçoamento de Pessoal de Nível Superior), Brazil",
     "https://sucupira.capes.gov.br/", "A1, A2, B1 to B5, C",
     "The classification of publication venues used by CAPES to assess graduate programmes in Brazil."),
    ("gii-grin-scie", "GII-GRIN-SCIE Conference Rating", "GII (Italy), GRIN (Italy) and SCIE (Spain)",
     "https://scie.lcc.uma.es/", "Class 1 to 3, W (work in progress), non-classified",
     "A rating of computer science conferences computed from other rankings and citation indicators."),
    ("ccf", "CCF Recommended List", "China Computer Federation",
     "https://www.ccf.org.cn/en/", "A, B, C",
     "The list of international conferences and journals recommended by the China Computer Federation."),
    ("h5-index", "Google Scholar h5-index", "Google Scholar Metrics",
     "https://scholar.google.com/citations?view_op=top_venues", "a number",
     "The largest number h such that h articles of the venue published in the last five complete years have at least "
     "h citations each."),
    ("h5-median", "Google Scholar h5-median", "Google Scholar Metrics",
     "https://scholar.google.com/citations?view_op=top_venues", "a number",
     "The median number of citations of the articles that make up the h5-index of the venue."),
]


def iri(name):
    return BASE + "/" + name


def generate(run):
    t = set()
    scheme = IRI(BASE)
    t.add((scheme, IRI(RDF_TYPE), IRI(SKOS + "ConceptScheme")))
    t.add((scheme, IRI(SKOS + "prefLabel"), Literal("Rating systems of conferences", None, "en")))
    for name, label, publisher, home, scale, definition in SYSTEMS:
        c = IRI(iri(name))
        t.add((c, IRI(RDF_TYPE), IRI(SKOS + "Concept")))
        t.add((c, IRI(SKOS + "inScheme"), scheme))
        t.add((c, IRI(SKOS + "topConceptOf"), scheme))
        t.add((c, IRI(SKOS + "prefLabel"), Literal(label, None, "en")))
        t.add((c, IRI(SKOS + "definition"), Literal(definition, None, "en")))
        t.add((c, IRI(SKOS + "scopeNote"), Literal("Scale: " + scale, None, "en")))
        t.add((c, IRI(DCT + "publisher"), Literal(publisher, None, None)))
        t.add((c, IRI(FOAF + "homepage"), IRI(home)))
    run.note(f"{len(SYSTEMS)} rating systems.")
    run.write_turtle("rating-systems.ttl.gz", t)
