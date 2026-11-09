# 0019 Academic fields (OECD FOS 2007) and disciplines (Wikidata items)

Status: accepted · Date: 2026-11-09

## Context

The search and the map filter by academic field and by discipline. The sources describe subjects in different ways:
ConfIDent assigns its own academic fields, each with a field of the OECD classification; the portal has 27 research
areas; Wikidata names main subjects; dblp is the bibliography of computer science; Springer publishes proceedings in
book series by subject. Kai agreed on 2026-11-09 to the OECD fields with a finer level of Wikidata items.

## Decision

- **Academic field** (`cr:field`): a field of the OECD classification of fields of science and technology (Frascati
  Manual, revised 2007): 6 major fields, 42 fields, published as the vocabulary `oecd-fos`. ConfIDent uses the same
  classification.
- **Discipline** (`cr:discipline`): a Wikidata item for a discipline or research topic, finer than the fields. Each
  discipline item gets a field where it can be derived.
- **`ls-fields`** (linkset) links the series and event records of the sources to fields and disciplines: ConfIDent's
  own mapping, its academic fields matched by name to Wikidata disciplines, the areas of the portal mapped by hand,
  the main subjects of Wikidata, computer science for dblp, the book series for Springer. The rules are in the
  generator.
- **`ids`** joins the fields and disciplines of the records. An event without its own takes those of its series; a
  series has its own and those of at least 30% of its events.
- Wikidata's subclass and part-of chains are followed one step only: longer chains lead almost every topic to almost
  every field.

## Consequences

Fields cover nearly all events, mostly through dblp. Disciplines are as fine as the sources: ConfIDent and Wikidata
give topics, dblp and Springer do not.
