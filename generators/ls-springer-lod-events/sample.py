"""Samples of the event linksets for judging (kg-commons 0032), from their matches files.

python3 generators/ls-springer-lod-events/sample.py <out dir> [size]

For every unit (linkset, cr:sameAs, target source) of the stable versions of the ls-*-events linksets, a random sample
(seed 2026; all links of a unit up to 150) with the facts of both events, in the format of cr sample-links (one
<unit>.jsonl per unit, units.json), so that cr link-quality reports the verdicts. The events of dblp have no records
of their own in our data; the matches files hold the facts of both sides.
"""

import csv
import gzip
import json
import random
import sys
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
from cr import catalog, config, project  # noqa: E402

SLUGS = ["ls-springer-lod-events", "ls-confref-portal-events", "ls-confident-events", "ls-wikidata-events"]


def main(out, size=100, small=150, seed=2026):
    cfg, cat = config.load(), catalog.Catalog()
    out.mkdir(parents=True, exist_ok=True)
    summary = []
    csv.field_size_limit(10 ** 7)
    for slug in SLUGS:
        v = cat.get(slug).stable
        units = defaultdict(list)
        with gzip.open(cfg.require("store") / slug / v / f"{slug}-matches.tsv.gz", "rt", encoding="utf-8") as f:
            for r in csv.DictReader(f, delimiter="\t"):
                units[r["target source"]].append(r)
        for target, rows in sorted(units.items()):
            name = f"{slug}--sameAs--{target}"
            rows = sorted(rows, key=lambda r: (r["source"], r["target"]))
            rnd = random.Random(f"{seed}:{name}")
            chosen = rows if len(rows) <= small else rnd.sample(rows, size)
            with open(out / f"{name}.jsonl", "w", encoding="utf-8") as f:
                for i, r in enumerate(chosen):
                    f.write(json.dumps({"i": i, "unit": name, "rule": r["rule"],
                                        "source": {"iri": r["source"], **json.loads(r["source facts"])},
                                        "target": {"iri": r["target"], **json.loads(r["target facts"])}},
                                       ensure_ascii=False) + "\n")
            summary.append({"unit": name, "dataset": slug, "property": project.ONTOLOGY + "sameAs", "source": target,
                            "links": len(rows), "sample": len(chosen)})
            print(f"{name:55} {len(rows):>7,} links, sample {len(chosen)}")
    (out / "units.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main(Path(sys.argv[1]), *(int(a) for a in sys.argv[2:3]))
