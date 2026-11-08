"""Harvest the GND records our datasets name, from the Linked Data Service of the DNB (the input of the generator).

python3 generators/gnd/harvest.py <out dir>

The numbers come from the stable versions of the datasets in selection.SOURCES (selection.py), read from the store;
then one step further: the records the harvested records name as place or related conference (selection.FOLLOW).
Every record is fetched as Turtle from https://d-nb.info/gnd/<n>/about/lds and saved unchanged as records/<n>.ttl;
status.json records for every number asked the number the DNB answered with (a redirect for a number that was
replaced) or null (not found). harvest.json: the datasets and versions read, the counts, the times. Resumable; about
fewer than 2 requests per second; the User-Agent of the project.
"""

import datetime
import json
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "src"))
sys.path.insert(0, str(Path(__file__).resolve().parent))
from cr import catalog, config  # noqa: E402
from cr.fetch import request  # noqa: E402
from cr.rdf import read_triples  # noqa: E402
import selection  # noqa: E402

LDS = "https://d-nb.info/gnd/{}/about/lds"
PAUSE = 0.15   # with the answer time of the DNB (about 0.5 s) under 2 requests per second


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def stable_files():
    cfg, cat = config.load(), catalog.Catalog()
    out, versions = {}, {}
    for slug in selection.SOURCES:
        v = cat.get(slug).stable
        folder = cfg.require("store") / slug / v
        out[slug] = sorted(p for p in folder.glob("*.ttl.gz") if not p.name.endswith("-meta.ttl.gz"))
        versions[slug] = v
    return out, versions


def fetch(out, status, n):
    """Fetch record n into records/<final number>.ttl; returns the final number or None."""
    if n in status:
        return status[n]
    for attempt in range(6):
        try:
            with urllib.request.urlopen(request(LDS.format(n)), timeout=60) as r:
                body, final = r.read(), r.geturl()
            break
        except urllib.error.HTTPError as e:
            if e.code == 404 or e.code == 410:
                status[n] = None
                time.sleep(PAUSE)
                return None
            if e.code < 500 and e.code != 429:
                raise
        except (urllib.error.URLError, TimeoutError):
            pass
        time.sleep(10 * (attempt + 1))
    else:
        raise SystemExit(f"giving up on {n}")
    m = selection.GND.match(final.split("/about")[0])
    number = m.group(1) if m else n
    path = out / "records" / f"{number}.ttl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    status[n] = number
    time.sleep(PAUSE)
    return number


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    status_path = out / "status.json"
    status = json.loads(status_path.read_text()) if status_path.exists() else {}
    files, versions = stable_files()
    report = {"service": LDS, "datasets": versions, "started": now()}
    seeds = selection.seeds(files)
    report["seeds"] = len(seeds)
    report["seeds_per_dataset"] = {s: sum(1 for v in seeds.values() if s in v) for s in selection.SOURCES}
    print(report, flush=True)
    for i, n in enumerate(sorted(seeds), 1):
        fetch(out, status, n)
        if i % 200 == 0:
            status_path.write_text(json.dumps(status, indent=0, sort_keys=True))
            print(f"{i:,}/{len(seeds):,}", flush=True)
    followed = set()
    for number in sorted({v for v in status.values() if v}):
        followed |= selection.followed(read_triples(out / "records" / f"{number}.ttl"))
    followed -= set(status)
    report["followed"] = len(followed)
    print("followed", len(followed), flush=True)
    for n in sorted(followed):
        fetch(out, status, n)
    status_path.write_text(json.dumps(status, indent=0, sort_keys=True))
    report["asked"] = len(status)
    report["not_found"] = sum(1 for v in status.values() if v is None)
    report["redirected"] = sum(1 for k, v in status.items() if v and v != k)
    report["finished"] = now()
    (out / "harvest.json").write_text(json.dumps(report, indent=1) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
