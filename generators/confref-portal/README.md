# confref-portal: generator history

The conferences of portal.confref.org (2019-2022), the confref prototype funded by the Digital Science Catalyst Grant.

## History

- 2019-04-29: portal.confref.org online (Net Wise / Thread Solutions, on the conference portal code donated by Springer
  Nature): PHP front end, Mule, MySQL; data from the Springer Nature metadata API (2002 on), from 2020 also from DBLP;
  API `/api/conferences/`, `/api/areas/`, `/api/countries/` (2019-07-08).
- 2020-07-11: Wolfgang Fahl downloads all conferences through the API (`confref-conferences.json`, 25,804,600 bytes);
  ConferenceCorpus keeps it (`https://github.com/WolfgangFahl/ConferenceCorpus/wiki/data/confref.tgz`, archive files
  dated 2021-06-03).
- 2021-12-13: the portal is taken offline (log4j); it came back without data and was not repaired. The code is lost.
- 2026-11-08: the archive registered as inputs:confref/portal-2020; this generator (decision 0010).

## The generator

True to the API (details in the docstring of `generate.py`): conferences, series and areas with a property per field
of the API in `data/confref-portal/vocab/`; HTML character references decoded; null fields left out.

## Known limits of the source (kept)

- Placeholder dates: start and end on 1 January of the year (6,365 conferences), sometimes start and end in different
  years (`bueroautomation1985`: 1983 to 1985).
- Impossible years (0, 19670).
- The series name of today on old events: merging Springer and DBLP gave every event the latest name and acronym of its
  series (BTW 1985 is "Datenbanksysteme für Business, Technologie und Web …"; TIB issue CONFIDENT-161).
- Rankings never filled; 45 conferences without research area; 757 of 5,668 series (1,128 conferences) without DBLP id.
