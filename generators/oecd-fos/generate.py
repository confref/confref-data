"""oecd-fos: the fields of science and technology of the OECD (Frascati Manual, revised 2007) as SKOS concepts
(decision 0019).

The classification "Revised Field of Science and Technology (FOS) Classification in the Frascati Manual" (OECD,
DSTI/EAS/STP/NESTI(2006)19/FINAL, 2007): 6 major fields and 42 fields, with their codes. ConfIDent uses it for its
academic fields. Each concept is https://id.confref.org/data/oecd-fos/<code> (skos:notation the code); the scheme is
https://id.confref.org/data/oecd-fos. Labels in English as in the classification, in German as in the German edition
of the Frascati Manual where it has them.
"""

from cr import project
from cr.rdf import IRI, RDF_TYPE, Literal

INPUTS = {}
PARAMS = {}

SKOS = "http://www.w3.org/2004/02/skos/core#"
DCT = "http://purl.org/dc/terms/"
BASE = project.DATA + "oecd-fos"

FOS = [
    ("1", "Natural sciences", "Naturwissenschaften"),
    ("1.1", "Mathematics", "Mathematik"),
    ("1.2", "Computer and information sciences", "Informatik und Informationswissenschaften"),
    ("1.3", "Physical sciences", "Physik"),
    ("1.4", "Chemical sciences", "Chemie"),
    ("1.5", "Earth and related environmental sciences", "Geowissenschaften und Umweltwissenschaften"),
    ("1.6", "Biological sciences", "Biologie"),
    ("1.7", "Other natural sciences", "Andere Naturwissenschaften"),
    ("2", "Engineering and technology", "Ingenieurwissenschaften und Technik"),
    ("2.1", "Civil engineering", "Bauingenieurwesen"),
    ("2.2", "Electrical engineering, electronic engineering, information engineering",
     "Elektrotechnik, Elektronik, Informationstechnik"),
    ("2.3", "Mechanical engineering", "Maschinenbau"),
    ("2.4", "Chemical engineering", "Chemieingenieurwesen"),
    ("2.5", "Materials engineering", "Werkstofftechnik"),
    ("2.6", "Medical engineering", "Medizintechnik"),
    ("2.7", "Environmental engineering", "Umwelttechnik"),
    ("2.8", "Environmental biotechnology", "Umweltbiotechnologie"),
    ("2.9", "Industrial biotechnology", "Industrielle Biotechnologie"),
    ("2.10", "Nano-technology", "Nanotechnologie"),
    ("2.11", "Other engineering and technologies", "Andere Ingenieurwissenschaften und Technik"),
    ("3", "Medical and health sciences", "Medizin und Gesundheitswissenschaften"),
    ("3.1", "Basic medicine", "Grundlagenmedizin"),
    ("3.2", "Clinical medicine", "Klinische Medizin"),
    ("3.3", "Health sciences", "Gesundheitswissenschaften"),
    ("3.4", "Medical biotechnology", "Medizinische Biotechnologie"),
    ("3.5", "Other medical sciences", "Andere medizinische Wissenschaften"),
    ("4", "Agricultural sciences", "Agrarwissenschaften"),
    ("4.1", "Agriculture, forestry, and fisheries", "Land- und Forstwirtschaft, Fischerei"),
    ("4.2", "Animal and dairy science", "Tierwissenschaften und Milchwirtschaft"),
    ("4.3", "Veterinary science", "Veterinärmedizin"),
    ("4.4", "Agricultural biotechnology", "Agrarbiotechnologie"),
    ("4.5", "Other agricultural sciences", "Andere Agrarwissenschaften"),
    ("5", "Social sciences", "Sozialwissenschaften"),
    ("5.1", "Psychology", "Psychologie"),
    ("5.2", "Economics and business", "Wirtschaftswissenschaften"),
    ("5.3", "Educational sciences", "Erziehungswissenschaften"),
    ("5.4", "Sociology", "Soziologie"),
    ("5.5", "Law", "Rechtswissenschaft"),
    ("5.6", "Political science", "Politikwissenschaft"),
    ("5.7", "Social and economic geography", "Sozial- und Wirtschaftsgeographie"),
    ("5.8", "Media and communications", "Medien- und Kommunikationswissenschaften"),
    ("5.9", "Other social sciences", "Andere Sozialwissenschaften"),
    ("6", "Humanities", "Geisteswissenschaften"),
    ("6.1", "History and archaeology", "Geschichte und Archäologie"),
    ("6.2", "Languages and literature", "Sprach- und Literaturwissenschaften"),
    ("6.3", "Philosophy, ethics and religion", "Philosophie, Ethik und Religion"),
    ("6.4", "Arts (arts, history of arts, performing arts, music)", "Kunst (Kunst, Kunstgeschichte, darstellende Kunst, Musik)"),
    ("6.5", "Other humanities", "Andere Geisteswissenschaften"),
]


def iri(code):
    return BASE + "/" + code


def generate(run):
    t = set()
    scheme = IRI(BASE)
    t.add((scheme, IRI(RDF_TYPE), IRI(SKOS + "ConceptScheme")))
    t.add((scheme, IRI(SKOS + "prefLabel"), Literal("Fields of science and technology (OECD FOS 2007)", None, "en")))
    t.add((scheme, IRI(SKOS + "prefLabel"), Literal("Wissenschaftszweige (OECD FOS 2007)", None, "de")))
    t.add((scheme, IRI(DCT + "source"), IRI("https://www.oecd.org/science/inno/38235147.pdf")))
    for code, en, de in FOS:
        c = IRI(iri(code))
        t.add((c, IRI(RDF_TYPE), IRI(SKOS + "Concept")))
        t.add((c, IRI(SKOS + "inScheme"), scheme))
        t.add((c, IRI(SKOS + "notation"), Literal(code, None, None)))
        t.add((c, IRI(SKOS + "prefLabel"), Literal(en, None, "en")))
        t.add((c, IRI(SKOS + "prefLabel"), Literal(de, None, "de")))
        if "." in code:
            parent = IRI(iri(code.split(".")[0]))
            t.add((c, IRI(SKOS + "broader"), parent))
            t.add((parent, IRI(SKOS + "narrower"), c))
        else:
            t.add((c, IRI(SKOS + "topConceptOf"), scheme))
            t.add((scheme, IRI(SKOS + "hasTopConcept"), c))
    run.note(f"{sum(1 for c, *_ in FOS if '.' not in c)} major fields, {sum(1 for c, *_ in FOS if '.' in c)} fields.")
    run.write_turtle("oecd-fos.ttl.gz", t)
