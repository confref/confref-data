# 0005 Our identifiers: opaque, short, with a check character, from one counter

Status: accepted · Date: 2026-11-08

## Context

Acronyms collide (several ICCC) and change; merges and splits must not break citations. The portal's IDs
(`btw2021`) and the Springer IRIs (`confseries/ppsn`, `conference/ppsn2014`) were readable but not persistent.
Random IDs would need a lookup for collisions and break deterministic generation; UUIDs are too long to cite.

## Decision

- **Form:** a type letter (`s` series, `e` event), a number written in lowercase Crockford base32 (`0-9a-z` without
  `i l o u`), and a **check character** (Luhn mod 32 over the same alphabet). Examples: `s10000y`, `e1093fb`.
  IRIs: `https://id.confref.org/series/<id>`, `…/event/<id>` ([0002](0002-iris-and-hosts.md)).
- **One counter for all types**, starting at 32⁴, so that IDs have five characters (plus type and check) up to about
  32 million, and the number alone never means two things.
- **Minted only by the generator of the identifier set `ids`**, like the entity pages of JudaicaLink
  (judaicalink-data 0022): the highest number of the previous set + 1 (kept in the run record), new entities numbered
  in a stable order (sorted by their smallest source record IRI), so runs are deterministic. Every ID ever issued,
  retired ones included, stays in the set (merged, split, withdrawn, with a date) and is checked against as a
  safeguard. No ID is ever reused.
- Should another place ever need to mint IDs, it gets a reserved range of numbers.
- Readable aliases (acronym slugs such as `eswc2016`, the legacy IRIs of lod.springer.com and lod.confref.org, the
  portal IDs) are lookups that redirect to the identifier; they are not identifiers.

## Consequences

Formatting and parsing an ID (with the check) is one function of the `ids` generator, so that a shared framework could
take the form as a parameter (deviation X2).
