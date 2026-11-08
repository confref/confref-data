"""The project this framework works for: names, base IRIs, our own ontology (project.toml, committed).

Everything that differs between the projects that share the framework is read from project.toml at the repository
root, and the modules take their constants from here, so that the code stays the same for all of them (deviation X1 in
kg-commons, projects/confref.md).
"""

import tomllib

from .config import ROOT

_P = tomllib.loads((ROOT / "project.toml").read_text(encoding="utf-8"))

NAME = _P["name"]                     # also the identifier source of our own IRIs
TITLE = _P["title"]
BASE = _P["base"]                     # our IRIs: datasets/, dumps/, data/
DATA = BASE + "data/"                 # records we coin
DATASETS = BASE + "datasets/"         # datasets (= graphs), versions, agents, vocabulary
LANDING_PAGE = _P["landing_page"]
FINDER = _P["finder"]
USER_AGENT = _P["user_agent"]
FRAMEWORK = _P["framework"]["name"]
FRAMEWORK_LABEL = _P["framework"]["label"]
REPOSITORY = _P["framework"]["repository"]
PREFIX = _P["ontology"]["prefix"]     # the prefix of our own terms
ONTOLOGY = _P["ontology"]["namespace"]
