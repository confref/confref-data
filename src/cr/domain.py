"""The domain tables of the project: domain.toml at the repository root (deviation X8 in kg-commons).

The sources and the forms of their IRIs, the identifiers in our data, the authority datasets, the classes, and the
tables of the link quality check. Everything else of the framework is the same for every project. Terms are written as
prefixed names (cr.turtle.PREFIXES and the [prefixes] of the file) or as full IRIs. The tests read tests/domain.toml
(environment variable CR_DOMAIN), so that they do not depend on the project.
"""

import os
import re
import tomllib
from pathlib import Path

from . import project
from .config import ROOT
from .turtle import PREFIXES as _OUTPUT_PREFIXES

PATH = Path(os.environ.get("CR_DOMAIN") or ROOT / "domain.toml")
_D = tomllib.loads(PATH.read_text(encoding="utf-8"))

# prefixes of the identity declarations and of this file, beyond cr.turtle.PREFIXES
PREFIXES = dict(_D.get("prefixes", {}))


def iri(term):
    """A term of the file as an IRI: "prefix:local", "<iri>" or an IRI as it is."""
    if term.startswith("<") and term.endswith(">"):
        return term[1:-1]
    if re.match(r"^[a-z][a-z0-9+.-]*://", term, re.I):
        return term
    prefix, sep, local = term.partition(":")
    ns = {**_OUTPUT_PREFIXES, **PREFIXES}.get(prefix) if sep else None
    if ns is None:
        raise ValueError(f"{PATH.name}: unknown prefix in {term!r}")
    return ns + local


def _regex(entry, key="pattern"):
    return re.compile(entry[key], re.I if "i" in entry.get("flags", "") else 0)


# cr.iris: (name, pattern of the variants, the canonical form, where the source states it); our own form comes first
FORMS = [(f["name"], _regex(f), f["canonical"], f["statement"]) for f in _D.get("form", [])]
# forms that are canonicalised but are not an identifier of a source of their own (identify skips them)
NOT_IDENTIFYING = {f["name"] for f in _D.get("form", []) if f.get("identify") is False}
# vocabulary namespaces in the form their publisher uses: (old prefix, canonical prefix, where the publisher states it)
VOCABULARIES = [(v["old"], v["new"], v["statement"]) for v in _D.get("vocabulary", [])]

# cr.identifiers: the sources an identity declaration can name, with the syntax of a literal identifier and how an
# identifier is normalised ("strip", "upper", "wiki-title")
SOURCES = {name: dict(s) for name, s in _D.get("source", {}).items()}
SYNTAX = {name: _regex(s, "syntax") for name, s in SOURCES.items() if "syntax" in s}
NORMAL = {name: s.get("normal", "strip") for name, s in SOURCES.items()}
# our records that are the identifier of a source: (source, pattern below project.DATA, one group: the identifier)
NAMESPACES = [(n["source"], re.compile(re.escape(project.DATA) + n["pattern"] + "$")) for n in _D.get("namespace", [])]
# IRIs of a source that are not canonicalised but name its identifiers (one group: the identifier)
ALIASES = [(a["source"], _regex(a)) for a in _D.get("alias", [])]
# properties whose literal value is an identifier of a source: "source", or {source = …, prefix = …} when the value
# lacks a part of the identifier (e.g. a dblp key without its "conf/")
_LP = {iri(k): (v if isinstance(v, dict) else {"source": v}) for k, v in _D.get("literal_properties", {}).items()}
LITERAL_PROPERTIES = {k: v["source"] for k, v in _LP.items()}
LITERAL_PREFIX = {k: v["prefix"] for k, v in _LP.items() if v.get("prefix")}
# IRI forms that name the identifiers of another source
SAME_IDENTIFIER = dict(_D.get("same_identifier", {}))
# statements by which a record of an authority dataset names itself in another source (besides owl:sameAs,
# skos:exactMatch and the literal properties)
IDENTITY = {iri(t) for t in _D.get("identity", [])}

# cr.authorities: authority dataset -> its sources; datasets whose links never select records
AUTHORITIES = {slug: tuple(srcs) for slug, srcs in _D.get("authorities", {}).items()}
NOT_LINKING = set(_D.get("not_linking", []))

# cr.classes: class -> kind; deprecated classes -> the class that replaces them; kinds that cannot be one thing
_C = _D.get("classes", {})
KINDS = {iri(k): v for k, v in _C.get("kind", {}).items()}
DEPRECATED_CLASSES = {iri(k): iri(v) for k, v in _C.get("deprecated", {}).items()}
CONTRADICTING = {frozenset(pair) for pair in _C.get("contradicting", [])}

# cr.linkquality: further candidate identity properties, the labels and facts shown as evidence, the authority
# datasets that hold the targets (source -> slug and namespace below project.DATA)
_L = _D.get("linkquality", {})
QUALITY_CANDIDATES = {iri(t) for t in _L.get("candidates", [])}
QUALITY_LABELS = {iri(t) for t in _L.get("labels", [])}
QUALITY_FACTS = {iri(k): v for k, v in _L.get("facts", {}).items()}
QUALITY_MAX = dict(_L.get("max", {}))
QUALITY_TARGETS = {src: dict(t) for src, t in _L.get("target", {}).items()}
