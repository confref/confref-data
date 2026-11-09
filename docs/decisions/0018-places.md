# 0018 Places: Wikidata items, matched by name where a source has only names

Status: accepted · Date: 2026-11-09

## Context

The map and the place filters of the platform need coordinates. Most sources give the place of an event as names
(Springer, the portal, ConfIDent: city and country; dblp: in the titles of its proceedings). Wikidata and the GND
name places as items. Kai agreed on 2026-11-09 to use Wikidata (CC0) as the gazetteer; GeoNames (CC BY) only for
gaps, as a dataset with its own licence.

## Decision

- **The place of an event is a Wikidata item** (`schema:location`), as specific as the source allows: a city, else a
  region, else a country. Online events have no place; their attendance mode says so.
- **`ls-places`** (linkset) links every event record of the sources to its place: the items named by Wikidata and the
  GND as they are; names matched to Wikidata by rules (city name in the country of the event, the best known
  candidate by its number of Wikipedia articles, settlements preferred, regions and countries only where the name
  means them). Quality is measured on samples, as for the identity links.
- **`wikidata-places`** (records) holds the places linked and their countries as Wikidata states them: coordinates,
  country, class, the administrative unit, ISO codes, population, labels.
- **The harvest** is an input (`inputs:wikidata/places-<date>`): the countries and subdivisions with their names, the
  candidates for every place name of the sources, and the statements of all candidates. A new version of a source
  needs a new harvest.
- **`ids`** takes the most specific place of the record first in precedence (0016) and keeps the name of the source
  where no item was found.

## Consequences

The map shows events at the coordinates of their city or region; events placed only by country are counted, not
shown as points. GeoNames is not used for now: Wikidata covers the names of the sources.
