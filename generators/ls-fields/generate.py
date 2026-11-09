"""ls-fields: the academic fields (OECD FOS 2007, dataset oecd-fos) and disciplines (Wikidata items) of the series
and event records of the sources (decision 0019).

Rules (fields.py for the tables):
1. ConfIDent (events and series, cf:Academic_Field): the field as ConfIDent states it for its academic field
   (cf:Academic_Field_OECD_FOS_2007, by its name); the discipline: the Wikidata item whose English or multilingual
   label or alias is the name of the academic field (compared without case and punctuation) and that is an academic
   discipline in Wikidata (an instance of a subclass of fields.DISCIPLINE_CLASSES) or an anchor item, among several
   the one with the most sitelinks; if none is, the best known item with that name (at least 5 sitelinks and three
   times as many as the next).
2. The portal (events, portal:area): the field and discipline of the area (fields.PORTAL_AREAS, curated).
3. Wikidata (events and series, wdt:P921 main subject): the topic as discipline, as stated.
4. dblp (conference venues and events): computer and information sciences (1.2): dblp is the bibliography of
   computer science.
5. Springer (conferences): the field of the book series of their proceedings (fields.BOOK_SERIES).
The field of a discipline: the field of its anchor (fields.ANCHORS), else the field ConfIDent gives to the academic
fields matched to it, else the field of a direct parent (wdt:P279, wdt:P361) that has one by the first two rules.

Writes cr:field (record or discipline -> OECD field) and cr:discipline (record -> Wikidata item), and
ls-fields-disciplines.tsv.gz: the academic fields of ConfIDent with the item chosen, the rule and the candidates.
"""

import gzip
import io
from collections import Counter, defaultdict

from cr import identifiers
from cr.generator import load_shared
from cr.rdf import IRI, RDF_TYPE, Literal

events = load_shared("ls-springer-lod-events", "events")
fields = load_shared("ls-fields", "fields")
fos = load_shared("oecd-fos", "generate")

INPUTS = {**events.INPUTS, "harvest": "inputs:wikidata/fields-2026-11-09"}
PARAMS = {}

CR = "https://id.confref.org/ontology/"
FIELD, DISCIPLINE = IRI(CR + "field"), IRI(CR + "discipline")
CF, PORTAL, SPR, W, WD = events.CF, events.PORTAL, events.SPR, events.W, events.WD
DBLP = events.DBLP


def harvest(run, name):
    for p in run.inputs("harvest"):
        if p.name == name:
            return p.read_text(encoding="utf-8").splitlines()[1:]
    raise FileNotFoundError(name)


def code_of_label():
    """ConfIDent's names of the OECD fields -> code."""
    return {fields.key(en): code for code, en, _de in fos.FOS} | {
        fields.key("Electrical Engineering, Electronic Engineering, Information Engineering"): "2.2",
        fields.key("Nano Technology"): "2.10", fields.key("Health Biotechnology"): "3.4",
        fields.key("Medical biotechnology"): "3.4", fields.key("Arts"): "6.4",
        fields.key("Agriculture, Forestry, Fisheries"): "4.1"}


def generate(run):
    by_label = code_of_label()
    names = defaultdict(set)
    for f in ("names-labels.tsv", "names-aliases.tsv"):
        for line in harvest(run, f):
            n, item = line.split("\t")
            names[fields.key(n)].add(item)
    sitelinks, disc = {}, set()
    for line in harvest(run, "candidates.tsv"):
        item, n, d = line.split("\t")
        sitelinks[item] = int(n or 0)
        if d == "1":
            disc.add(item)
    parents = defaultdict(set)
    for line in harvest(run, "parents.tsv"):
        i, p = line.split("\t")
        parents[i].add(p)
    anchors = {WD + q: code for q, code in fields.ANCHORS.items()}

    # 1. ConfIDent
    cls, lab, cf_fos, cf_field = {}, {}, {}, defaultdict(set)
    for s, p, o in run.triples("confident"):
        if p == RDF_TYPE:
            cls[str(s)] = str(o)
        elif p.endswith("#label"):
            lab[str(s)] = o.value
        elif p == CF + "Academic_Field_OECD_FOS_2007":
            cf_fos[str(s)] = o.value
        elif p == CF + "Academic_Field" and not isinstance(o, Literal):
            cf_field[str(s)].add(str(o))
    rows = ["academic field\tname\tOECD field\titem\trule\tcandidates"]
    page_item, page_code = {}, {}
    for page in sorted(s for s, c in cls.items() if c == CF + "Category_Academic_Field"):
        name = lab.get(page, "")
        code = by_label.get(fields.key(cf_fos.get(page, "")))
        if code:
            page_code[page] = code
        cands = sorted(i for i in names.get(fields.key(name), ()) if "/entity/Q" in i)
        ok = [i for i in cands if i in disc or i in anchors]
        rank = sorted(cands, key=lambda i: (-sitelinks.get(i, 0), int(i.rsplit("Q", 1)[1])))
        item, rule = None, "none"
        if ok:
            item = sorted(ok, key=lambda i: (-sitelinks.get(i, 0), int(i.rsplit("Q", 1)[1])))[0]
            rule = "discipline by name" if len(ok) == 1 else "discipline by name, most sitelinks"
        elif rank and sitelinks.get(rank[0], 0) >= 5 and (
                len(rank) == 1 or sitelinks.get(rank[0], 0) >= 3 * max(1, sitelinks.get(rank[1], 0))):
            item, rule = rank[0], "topic by name, clearly the best known"
        if item:
            page_item[page] = item
        rows.append("\t".join((page, name, code or "", item or "", rule, str(len(cands)))))
    # the field of a discipline item
    votes = defaultdict(Counter)
    for page, item in page_item.items():
        if page in page_code:
            votes[item][page_code[page]] += 1

    def field_of(item, depth=0):
        if item in anchors:
            return anchors[item]
        if votes.get(item):
            return votes[item].most_common(1)[0][0]
        if depth == 0:
            got = Counter(f for p in parents.get(item, ()) for f in [field_of(p, 1)] if f)
            return got.most_common(1)[0][0] if got else None
        return None

    out = set()
    stats = Counter()

    def put(record, codes=(), items=(), why=""):
        for c in codes:
            if c:
                out.add((IRI(record), FIELD, IRI(fos.iri(c))))
                stats[why + " field"] += 1
        for i in items:
            if i:
                out.add((IRI(record), DISCIPLINE, IRI(i)))
                stats[why + " discipline"] += 1

    for rec, pages in cf_field.items():
        if cls.get(rec) in (CF + "Category_Event", CF + "Category_Event_Series"):
            put(rec, {page_code.get(p) for p in pages}, {page_item.get(p) for p in pages}, "confident")
    # 2. the portal
    area_label, rec_areas = {}, defaultdict(set)
    for s, p, o in run.triples("portal"):
        if p.endswith("#label") and "/confref-portal/area/" in str(s):
            area_label[str(s)] = o.value
        elif p == PORTAL + "area":
            rec_areas[str(s)].add(str(o))
    for rec, areas in rec_areas.items():
        for a in areas:
            codes, q = fields.PORTAL_AREAS.get(area_label.get(a, ""), ([], None))
            put(rec, codes, [WD + q] if q else [], "confref-portal")
    # 3. Wikidata
    topics = defaultdict(set)
    for s, p, o in run.triples("wikidata"):
        if p == W + "P921" and str(o).startswith(WD + "Q"):
            topics[str(s)].add(str(o))
    _uf, evs = events.read(run)
    wd_records = {e.iri for e in evs.values() if e.source == "wikidata"}
    wd_series = set()
    for s, p, o in run.triples("wikidata"):
        if p in (W + "P8926",) or (p == W + "P31" and str(o) == WD + "Q47258130"):
            wd_series.add(str(s))
    for rec, items in topics.items():
        if rec in wd_records or rec in wd_series:
            put(rec, (), items, "wikidata")
    # 4. dblp
    for e in evs.values():
        if e.source == "dblp-event":
            put(e.iri, ["1.2"], (), "dblp")
    venues = set()
    for s, p, o in run.triples("dblp"):
        if p == DBLP + "publishedInStream":
            x = identifiers.identify(o)
            if x and x[0] == "dblp-venue" and x[1].startswith("conf/"):
                venues.add(str(o))
    for v in venues:
        put(v, ["1.2"], (), "dblp")
    # 5. Springer
    acr, proc = {}, defaultdict(set)
    for s, p, o in run.triples("springer"):
        if p == SPR + "bookSeriesAcronym":
            acr[str(s)] = o.value
        elif p == SPR + "proceedingsOf":
            proc[str(o)].add(str(s))
    for conf, books in proc.items():
        put(conf, {c for b in books for c in fields.BOOK_SERIES.get(acr.get(b, ""), [])}, (), "springer-lod")
    # the field of every discipline named
    named = {o for _s, p, o in out if p == DISCIPLINE}
    for item in named:
        f = field_of(str(item))
        if f:
            out.add((item, FIELD, IRI(fos.iri(f))))
            stats["discipline with field"] += 1
    buf = io.BytesIO()
    with gzip.GzipFile(filename="", mode="wb", fileobj=buf, compresslevel=9, mtime=0) as f:
        f.write(("\n".join(rows) + "\n").encode("utf-8"))
    run.path("ls-fields-disciplines.tsv.gz").write_bytes(buf.getvalue())
    matched = sum(1 for r in rows[1:] if r.split("\t")[3])
    run.note(f"ConfIDent academic fields matched to a Wikidata discipline: {matched:,} of {len(rows) - 1:,}; "
             f"disciplines named {len(named):,}. Statements: " + ", ".join(f"{k} {v:,}" for k, v in sorted(stats.items())))
    run.write_turtle("ls-fields.ttl.gz", out)
