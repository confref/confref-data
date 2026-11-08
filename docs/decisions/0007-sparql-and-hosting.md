# 0007 Fuseki; local development first, two VMs later

Status: accepted · Date: 2026-11-08

## Decision

- **SPARQL: Apache Jena Fuseki, read-only**, loaded and checked by the platform of the framework. Other engines
  (QLever) only for analysis, outside the platform.
- **Development is local** (a Lima VM, when the platform is set up).
- **Later two VMs on the university servers** (created by Kai Eckert when we are ready): the stable project website
  `confref.org` (catalogue, dumps, news) and the showcase VM `labs.confref.org` (platform: SPARQL, resolution of
  `id.confref.org`, dashboard, showcases), set up from the repositories. DNS of confref.org is moved from HdM
  Stuttgart then.
