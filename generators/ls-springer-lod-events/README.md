# The event linksets (ls-*-events)

`events.py` holds the rules shared by `ls-springer-lod-events`, `ls-confref-portal-events`, `ls-confident-events` and
`ls-wikidata-events` (read its docstring). Each linkset holds the links from the events of its source to those of the
sources after it in `events.SOURCES` (Springer, portal, ConfIDent, Wikidata, dblp), so that every pair of sources is
linked once and measured as a unit of its own (dataset, `cr:sameAs`, target source).
