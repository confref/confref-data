# Place links: quality of the name matching (2026-11-09)

The rules of `ls-places` (decision 0018) for place names were checked on a random sample of 300 links made by the
name rules (city or region), drawn from the 113,142 such links of the run of 2026-11-09 before the last change of the
rules. Each link was judged by an LLM (Claude, in Claude Code) on the evidence shown: the source, the city, region and
country as written, the Wikidata item chosen with its label, country and number of sitelinks, and the number of
candidates.

| Result | Links |
|---|---|
| correct | 297 |
| wrong | 1 |
| undecidable | 2 |

- Wrong: "Taipei, Taiwan" (dblp) linked to the country Taiwan, because Taiwan has "Taipei" among its aliases and more
  sitelinks than the city. The rules were changed: a country weighs a quarter of its sitelinks against a city of the
  same name. All 561 mentions of Taipei now go to the city.
- Undecidable: "Newport, USA" (47 candidates) and "Gloucester, USA" (7 candidates), names of several towns in the
  United States without a state; the best known town is chosen. Mentions with a state are not yet narrowed by it.

Accuracy 0.990 (297 of 300), 95% interval 0.971–0.997. The links made from items (Wikidata, GND) were not sampled:
they are the statements of the sources.

## Coverage (version 2026-11-09)

| Source | City | Region | Country | None |
|---|---|---|---|---|
| springer-lod | 8,850 | 65 | 406 | 6 |
| confref-portal | 36,005 | 199 | 1,628 | 113 |
| confident | 16,149 | 201 | 557 | 3,087 |
| dblp (titles) | 54,779 | 731 | 3,984 | 1,046 |
| wikidata (items) | 8,158 | | 160 | 2 |
| gnd (items) | 7,907 | | | |

ConfIDent's mentions without a place are mostly online events without a city.
