"""The classes of the entities in our data (the common layer, the ontology of the project).

The classes and their kinds come from domain.toml; readers use kind(), which also knows the deprecated classes and
the classes that replace them.
"""

from . import domain

KIND = domain.KINDS                    # class -> kind (e.g. Person, Place, Series, Event)
CLASS = {k: c for c, k in KIND.items()}   # kind -> the class to write
DEPRECATED = domain.DEPRECATED_CLASSES   # deprecated class -> the class that replaces it


def current(cls):
    """The class to write for a class (a deprecated one replaced)."""
    return DEPRECATED.get(cls, cls)


def kind(cls):
    """The kind of a class, for the current and the deprecated classes; None for other classes."""
    return KIND.get(current(cls))
