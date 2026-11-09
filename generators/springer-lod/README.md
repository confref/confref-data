# springer-lod: generator history

The conference data of lod.springer.com (Springer LOD pilot, 2014-2018), as of 2018-06-04. Also holds the module
`springer.py` shared by springer-lod, springer-lod-2015 and tuwien-pc.

## History

- 2014-11: lod.springer.com goes live (Springer, University of Mannheim: Volha Bryl, Kai Eckert; Net Wise: Andrey
  Gromyko): Fuseki and Pubby, data from Springer's production database (DDS) converted with Java (TSVtoRDF);
  public launch 2015-03-05; from 2015 a nightly sync with DDS by Net Wise.
- 2016-2017: GND ids (6,805 of 11,399 events matched by Maral Dadvar, HdM), ratings (CORE, CCF, QUALIS matched by
  Marija Grozdanic, Springer), Google Scholar metrics, review statistics; books and chapters added to the same graph.
- 2018-06-13: the dump (`gromyko.name/dwnld/lodspringerdump.zip`, files of 2018-06-04) handed over for confref;
  2018-08-17 loaded at lod.confref.org with every "springer.com" replaced by "confref.org"
  (inputs:springer/lod-2018-confref; the server copy was lost in 2018-10). lod.springer.com went offline later.
- 2026-11-08: the dump registered as inputs:springer/lod-2018; this generator (decision 0010).

## The dump

`conferences.ttl` (2,325,432,794 bytes, Jena's Turtle layout): 1,764 `ConferenceSeries`, 9,327 `Conference`, 59,684
`Book`, 1,251,627 `BookChapter`, one `void:Dataset`; `ontology.ttl`: the Springer LOD ontology (classes Book,
BookChapter, Conference, ConferenceRatingCCF/CORE/GIIGRIN/QUALIS, ConferenceSeries, ProceedingsVolume; 70 properties).
VoID: `dc:rights "CC0"`; the About page of lod.springer.com stated "freely available under CC0 1.0 Universal license"
(Wayback capture of 2015-03-29).

## The generator

- springer-lod.ttl.gz: every triple of conferences.ttl whose subject is not a chapter (`data/bookchapter/…`).
- springer-lod-ontology.ttl.gz: ontology.ttl.
- springer-lod-confref-2018.ttl.gz: for every lod.springer.com IRI of the two files its IRI in the lod.confref.org copy
  of 2018 (`owl:sameAs`; `owl:equivalentClass`/`owl:equivalentProperty` for the ontology terms). The copy was compared
  with the dump on 2026-11-08: apart from Windows line endings it is the dump with every "springer.com" replaced by
  "confref.org", which also turned the 59,065 links `link.springer.com/<ISBN>` into `link.confref.org/<ISBN>` (never a
  real address). So only the IRIs differ, and both IRI sets are kept without the broken links (decision 0010).
- True to the source (`springer.py`): `dc:` elements as `dcterms:` (the dataset description), GND IRIs with https.

## Known oddities of the source (kept)

- Literals with a language tag `@en` on almost every value, including acronyms, DOIs and names.
- `copyrightHolder` values typed `xsd:integer` although they are names ("Springer International Publishing
  Switzerland"^^xsd:integer, mostly on chapters).
- `googleScholarCategory` typed `rdfs:literal`.
- DBLP ids as `http://dblp.org/db/conf/<key>` (the old form; today `https://dblp.org/streams/conf/<key>`).
