"""The classes of the entities in our data (the common layer, judaicalink-ontology).

Generators write PERSON, ORGANISATION, PLACE, WORK, SUBJECT; readers use kind(), which also knows the deprecated
cr:Place, cr:Work, cr:Subject (and cr:Person, never defined).
"""

from . import project
from .turtle import PREFIXES

FOAF, SCHEMA, SKOS = (PREFIXES[p] for p in ("foaf", "schema", "skos"))
JL = project.ONTOLOGY

PERSON = FOAF + "Person"
ORGANISATION = FOAF + "Organization"
PLACE = SCHEMA + "Place"
WORK = SCHEMA + "CreativeWork"
SUBJECT = SKOS + "Concept"

# deprecated classes and what replaces them (cr:Person was never defined; rujen used it)
DEPRECATED = {JL + "Place": PLACE, JL + "Work": WORK, JL + "Subject": SUBJECT, JL + "Person": PERSON}

KIND = {PERSON: "Person", ORGANISATION: "Organization", PLACE: "Place", WORK: "Work", SUBJECT: "Subject"}


def current(cls):
    """The class to write for a class (a deprecated one replaced)."""
    return DEPRECATED.get(cls, cls)


def kind(cls):
    """Person, Organization, Place, Work, Subject or None, for the current and the deprecated classes."""
    return KIND.get(current(cls))
