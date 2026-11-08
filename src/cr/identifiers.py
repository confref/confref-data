"""The identifiers of external sources in our data (kg-commons 0029): which dataset names which identifier.

identify(term) gives (source, identifier) for an IRI of a known source in any of its forms (cr.iris), for our
records in an authority namespace (data/gnd/<n> is GND n, data/geonames/<n> is GeoNames n), and for a literal of an
identifier property (gndo:gndIdentifier). scan(run, inputs) lists, per source and identifier, the datasets that
name it as object; a subject is a statement about a record, not a link to it. Of the authority datasets only the
identity statements count (selects).
"""

import re
from collections import defaultdict
from urllib.parse import unquote

from . import domain, iris, project
from .rdf import BNode, Literal

JL = project.DATA   # records we coin
# the tables of the project (domain.toml): our records that are the identifier of a source, properties whose literal
# value is an identifier, IRI forms that name the identifiers of another source, the syntax of literal identifiers
AUTHORITY_NAMESPACES = domain.NAMESPACES
LITERAL_PROPERTIES = domain.LITERAL_PROPERTIES
SAME_IDENTIFIER = domain.SAME_IDENTIFIER
SYNTAX = domain.SYNTAX
# the authority datasets (cr.authorities) and the statements by which a record of one names itself in another source
AUTHORITY_DATASETS = set(domain.AUTHORITIES)
WDTN = "http://www.wikidata.org/prop/direct-normalized/"
IDENTITY = {"http://www.w3.org/2002/07/owl#sameAs", "http://www.w3.org/2004/02/skos/core#exactMatch",
            *LITERAL_PROPERTIES, *domain.IDENTITY}


# the sources an identity declaration can name (catalogue field "identity")
SOURCES = set(domain.SOURCES) | {project.NAME}   # project.NAME: links between our own records (no authority namespace)
# prefixes of the declarations beyond cr.turtle.PREFIXES
DECLARATION_PREFIXES = domain.PREFIXES
_declared = {}


def expand(term):
    """The IRI of a property of a declaration: "prefix:local", or "<iri>"; None if the prefix is unknown."""
    from .turtle import PREFIXES
    if term.startswith("<") and term.endswith(">"):
        return iris.canonical(term[1:-1])   # the variants of a vocabulary are one property (http and https GND)
    prefix, sep, local = term.partition(":")
    ns = {**PREFIXES, **DECLARATION_PREFIXES}.get(prefix) if sep else None
    return iris.canonical(ns + local) if ns else None


def declared(slug):
    """{property IRI (canonical form): {sources}}: the identity declaration of the dataset (catalogue field
    "identity", kg-commons 0032): which properties of the dataset state that a record is the same as a record of which
    source. A dataset without a declaration states no identity."""
    if slug not in _declared:
        from . import catalog
        e = catalog.Catalog().get(slug)
        table = (e.data.get("identity") if e else None) or {}
        _declared[slug] = {expand(k): frozenset(v) for k, v in table.items() if expand(k)}
    return _declared[slug]


def identity(slug, predicate, source):
    """Whether a statement of the dataset slug with this predicate, naming an identifier of source, states identity."""
    return source in declared(slug).get(iris.canonical(str(predicate)), ())


_quality = {}


def below_threshold(slug, predicate, source):
    """Whether the measured quality of this unit (catalog/link-quality.toml, kg-commons 0032) is below the threshold:
    accuracy under the threshold, or, when only a sample was checked, the lower bound of its interval under the
    threshold of the lower bound. A unit not measured is not below."""
    if not _quality:
        import tomllib
        from . import catalog
        path = catalog.CATALOG / "link-quality.toml"
        d = tomllib.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
        _quality["threshold"] = (d.get("accuracy", 0), d.get("lower", 0))
        for u in d.get("unit", []):
            prop = expand(u["property"])
            if prop:
                _quality[(u["dataset"], prop, u["source"])] = u
    u = _quality.get((slug, iris.canonical(str(predicate)), source))
    if not u:
        return False
    acc, low = _quality["threshold"]
    return u["accuracy"] < acc or (u.get("sample", 0) < u.get("links", 0) and u["lower"] < low)


def joins(slug, predicate, source):
    """Whether a statement joins records (linksets, entity pages): declared identity of a unit not below the
    threshold of the measured link quality (kg-commons 0032); below it, the link is kept but joins nothing."""
    return identity(slug, predicate, source) and not below_threshold(slug, predicate, source)


def selects(slug, predicate, source=None):
    """Whether a statement of the dataset slug selects the records it names in the authority datasets (kg-commons 0029):
    every statement of our datasets (also places of birth, occupations), of the authority datasets only their declared
    identity statements (otherwise the cascade would follow the places, occupations and related persons of authority
    records)."""
    if slug not in AUTHORITY_DATASETS:
        return True
    d = declared(slug).get(iris.canonical(str(predicate)), ())
    return source in d if source else bool(d)


def normal(source, identifier):
    """The identifier in the form we compare it: as the domain says for its source ("upper", "wiki-title"), else
    stripped."""
    how = domain.NORMAL.get(source, "strip")
    if how == "wiki-title":
        return wiki_title(identifier.strip())
    return identifier.strip().upper() if how == "upper" else identifier.strip()


# characters of a title that an IRI path cannot hold as they are (our records data/dbpedia/<lang>/<title>, kg-commons 0031)
_TITLE_ESCAPE = re.compile(r'[\x00-\x20<>"{}|\\^`?#%]')


def iri_part(source, identifier):
    """The identifier as the last part of the IRI of our record of it (data/<namespace>/<part>): a Wikipedia title
    escaped (title_iri_part), the others as they are."""
    return title_iri_part(identifier) if domain.NORMAL.get(source) == "wiki-title" else identifier


def title_iri_part(title):
    """A Wikipedia title (underscores) as the last part of an IRI: the characters an IRI cannot hold escaped."""
    return _TITLE_ESCAPE.sub(lambda m: "%{:02X}".format(ord(m.group(0))), title.replace(" ", "_"))


# IRIs that name the identifiers of a source without a canonical form of their own (domain.toml, e.g. Wikipedia
# articles and DBpedia resources, one source per language, kg-commons 0031)
WIKI = domain.ALIASES


def wiki_title(t):
    return unquote(t).replace(" ", "_")


def identify(term, predicate=None):
    """(source, identifier) or None."""
    if isinstance(term, Literal):
        source = LITERAL_PROPERTIES.get(predicate)
        value = domain.LITERAL_PREFIX.get(predicate, "") + term.value.strip() if source else ""
        if source and term.value.strip() and (source not in SYNTAX or SYNTAX[source].match(value)):
            return source, normal(source, value)
        return None
    if not isinstance(term, str) or isinstance(term, BNode):
        return None
    for source, pattern in AUTHORITY_NAMESPACES:
        m = pattern.match(term)
        if m:
            return source, normal(source, m.group(1))
    for name, pattern in WIKI:
        m = pattern.match(term)
        if m:
            return name, wiki_title(m.group(1))
    for name, pattern, _form, _src in iris.FORMS:
        if name == project.NAME or name in domain.NOT_IDENTIFYING:
            continue
        m = pattern.match(term)
        if m:
            name = SAME_IDENTIFIER.get(name, name)
            return name, normal(name, m.group(1))
    return None


def source_of(term, predicate=None):
    """identify(), and for one of our records outside the authority namespaces (the project name, the IRI)."""
    x = identify(term, predicate)
    if x is None and isinstance(term, str) and not isinstance(term, (Literal, BNode)) and \
            iris.canonical(term).startswith(JL):
        return project.NAME, iris.canonical(term)
    return x


def scan(run, inputs, sources=None):
    """{source: {identifier: {dataset}}} for the identifiers the inputs name as objects. inputs: {input name:
    "<slug>/<version>"} (e.g. cr.generator.stable_inputs); sources: only these sources."""
    found = defaultdict(lambda: defaultdict(set))
    for name, ref in inputs.items():
        slug = ref.split("/", 1)[0]
        for _s, p, o in run.triples(name):
            x = identify(o, p)
            if x and not selects(slug, p, x[0]):
                continue
            if x and (sources is None or x[0] in sources):
                found[x[0]][x[1]].add(slug)
    return found


def is_ours(term):
    """An IRI of the project (any form): never evidence when it comes from an external source (kg-commons 0029)."""
    return isinstance(term, str) and not isinstance(term, BNode) and iris.kind(term) == project.NAME
