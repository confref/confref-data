# 0015 Joint and co-located events: every way of the sources is kept

Status: accepted · Date: 2026-11-08 · Amends [0013](0013-series-and-events.md)

## Context

0013 models a joint event as one event in the series of each partner. AEON and ConfIDent model it as separate events
linked to each other (AEON "joint event of", ConfIDent `joint_venture_with`), and both know co-located events and
umbrella events. Joint conferences differ in practice: some are branded and run as one event, others present as a
collection of conferences under a common frame. The data of the sources should stay as the sources state it.

## Decision

- **All three ways are allowed, also side by side in our data:**
  - one event in several series (`cr:inSeries`, 0013): a joint conference that is branded and run as one event;
  - events held at a larger event (`cr:heldAt`, 0013, now also for this case): the partner conferences of a joint
    conference that presents as a collection, linked to the joint event that frames them; a workshop at its main
    conference; a conference at a federated event;
  - separate events linked to each other: `cr:jointWith` (held together, with joint organisation or programme) and
    `cr:colocatedWith` (same place and time, each with its own programme). Both are symmetric.
- A record of a source is mapped to the relation the source states; confref does not convert one way into another.
  The links show how the events and series are connected.
- The terms of AEON and ConfIDent are recorded in the ontology as close matches (`skos:closeMatch`), not reused as
  classes or properties (AEON is a work in progress and defines a series as a kind of event).

## Consequences

The same joint conference can appear as one event in two series (e.g. from dblp or Wikidata) and as two events
joint with each other (e.g. from ConfIDent). Whether such records are the same event is decided by the identity
links (phase 3), not by the model.
