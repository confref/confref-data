# 0013 Series and events: the model

Status: accepted · Date: 2026-11-08

## Context

The sources describe conferences at different levels. dblp's unit is the proceedings volume within a conference
stream: one conference can have several volumes, co-located workshops have volumes of their own, and a volume can
cover several workshops. Springer, ConfIDent and Wikidata describe the meeting itself. The identifiers
([0005](0005-identifiers.md)) need one level for series and one for events, and relations between them that hold for
workshops and joint events as well.

## Decision

- **A series** (`series/<id>`) is a sequence of events under one name that recur: a conference series, a workshop
  series, a symposium series. A workshop series is a series of its own, independent of the series of the events that
  host its editions.
- **An event** (`event/<id>`) is one meeting: a conference, a workshop, a symposium, a joint or federated event, at one
  time, in one place or online.
- **Proceedings are not events.** They are linked to the events whose contributions they publish: an event can have
  several volumes, and a volume can cover several events (e.g. the joint proceedings of several workshops).
- **Relations, both many-to-many:**
  - *in series* (event → series): the series an event belongs to. A joint event belongs to the series of each partner
    (e.g. a joint conference of two series).
  - *held at* (event → event): the event that hosts it: a workshop at its main conference, a conference at a federated
    event. A workshop series can move between hosts, so its editions are held at events of different series.
  - Series membership and hosting are independent: the series of a workshop is not derived from its host.
- Renamed series stay one series (with the former names as alternative names). Mergers and splits of series, and
  tracks or sessions within an event, are not modelled for now.
- The terms are defined in the ontology ([0014](0014-landing-pages-iris-ontology.md)); reused vocabularies first,
  our own terms where nothing fits.

## Consequences

Each record of a source is mapped to one level: dblp conference streams to series, dblp proceedings to proceedings
(their dblp event IDs, where present, to events); ConfIDent event series and events, Springer conference series and
conferences, Wikidata conference series and conferences to series and events. The identity links of phase 3 join
records only at the same level.
