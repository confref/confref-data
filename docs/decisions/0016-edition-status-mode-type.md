# 0016 Facts of an event: edition number, status, attendance mode, type

Status: accepted · Date: 2026-11-08 · Amends [0013](0013-series-and-events.md)

## Context

ConfIDent records an ordinal, a status (as scheduled, postponed, canceled, to be confirmed), a mode (on site, online,
hybrid) and, in DataCite, a type (Academic Conference, Workshop, …) for its events; Wikidata and other sources have
some of these. An event can belong to several series ([0017](0017-joint-and-colocated-events.md)), and then it has an
edition number in each.

## Decision

- **Edition number:** `cr:edition` on the event when it belongs to one series. When it belongs to several, one
  `cr:Edition` per series (`cr:hasEdition`), with the series (`cr:editionOf`) and the number (`cr:editionNumber`).
  The IRI of an edition of our identifier set is `event/<id>/edition/<series id>`; a dataset that records editions
  for its own records coins them below `data/<namespace>/`.
- **Status and attendance mode:** schema.org, `schema:eventStatus` (`EventScheduled`, `EventPostponed`,
  `EventCancelled`, `EventRescheduled`, `EventMovedOnline`) and `schema:eventAttendanceMode` (`Offline…`,
  `Online…`, `MixedEventAttendanceMode`). A value without a schema.org equivalent (ConfIDent's "to be confirmed") is
  kept only in the dataset of its source.
- **Cancelled and postponed events keep their identifiers.** Calls for papers and sometimes proceedings refer to them.
- **Type:** `cr:eventType`, with the type classes of AEON as values (academic conference, workshop, symposium,
  congress, colloquium, forum, seminar, tutorial, hackathon), the types that ConfIDent and DataCite use. A property,
  not `rdf:type`: AEON is a work in progress, and its classes are not our classes. The type belongs to the event; a
  series has no type of its own (series change their names, e.g. from workshop to conference).

## Consequences

The ontology defines `cr:edition`, `cr:Edition`, `cr:hasEdition`, `cr:editionOf`, `cr:editionNumber` and
`cr:eventType`, and describes the reused schema.org terms. The IRI scheme (0014) gets the path
`event/<id>/edition/<series id>`.
