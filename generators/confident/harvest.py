"""Harvest ConfIDent completely (the input of the generator, decision 0011).

python3 generators/confident/harvest.py <out dir>

Saves every response of the API unchanged, so that the generator reads exactly what ConfIDent said:

- ask/<query>/<n>.json: the semantic data through the SMW Ask API, 250 results per request, for the categories of
  pages (Event, Event Series, Organization, Academic Field, Country) and of subobjects (Organizer, Deadline,
  Maintainer), each with every typed property of the wiki (properties.json) and the modification and creation date;
  subobjects with their page (?-Has subobject).
- properties.json: the properties of the wiki with their types.
- pages/<namespace>-<redirects|pages>/<n>.json: page ID and title of every page of the five namespaces (the page ID
  survives moves; it names our records).
- log/<type>-<namespace>/<n>.json: the deletions, moves and merges in the five namespaces (to follow ConfIDent's
  curation).
- harvest.json: what was fetched, when, and the counts.

An interrupted harvest continues (files already there are kept); for a new harvest use a new directory. One request
per second; the User-Agent of the project (project.toml, judaicalink-data 0028).
"""

import datetime
import json
import sys
import time
import urllib.parse
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[2] / "src"))
from cr.fetch import get  # noqa: E402

API = "https://www.confident-conference.org/api.php"
NAMESPACES = {7100: "Event_Series", 7200: "Event", 7300: "Academic_Field", 7400: "Country", 7500: "Organization"}
PAGE_CATEGORIES = ["Event", "Event Series", "Organization", "Academic Field", "Country"]
SUBOBJECT_CATEGORIES = ["Organizer", "Deadline", "Maintainer"]
LIMIT = 250   # larger pages time out on the server (1,000 results with all properties: 21 s; 250: 2 s)


def now():
    return datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")


def fetch(path, params):
    """The response for params, from path if it is there, else from the API (saved to path)."""
    if path.exists():
        return json.loads(path.read_bytes())
    body = get(API + "?" + urllib.parse.urlencode({**params, "format": "json"}))
    data = json.loads(body)
    if "error" in data:
        raise SystemExit(f"API error for {params}: {data['error']}")
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_bytes(body)
    time.sleep(1)
    return data


def properties(out):
    data = fetch(out / "properties.json", {"action": "ask", "query": "[[Property:+]]|?Has type|limit=1000"})
    typed = sorted(k.split(":", 1)[1] for k, v in data["query"]["results"].items() if v["printouts"].get("Has type"))
    return typed


def ask(out, name, condition, printouts):
    folder, n, offset, results = out / "ask" / name.replace(" ", "_"), 1, 0, 0
    while True:
        query = "|".join([condition, *(f"?{p}" for p in printouts), f"limit={LIMIT}", f"offset={offset}"])
        data = fetch(folder / f"{n:03d}.json", {"action": "ask", "query": query})
        results += len(data.get("query", {}).get("results") or {})
        nxt = data.get("query-continue-offset")
        if not nxt:
            return results
        offset, n = nxt, n + 1


def listing(out, folder, params, key, cont):
    n, items, extra = 1, 0, {}
    while True:
        data = fetch(out / folder / f"{n:03d}.json", {**params, **extra})
        items += len(data["query"][key])
        if "continue" not in data:
            return items
        extra, n = {cont: data["continue"][cont], "continue": data["continue"]["continue"]}, n + 1


def main(out):
    out.mkdir(parents=True, exist_ok=True)
    report = {"api": API, "started": now(), "ask": {}, "pages": {}, "log": {}}
    typed = properties(out)
    printouts = typed + ["Modification date", "Creation date"]
    for c in PAGE_CATEGORIES:
        report["ask"][c] = ask(out, c, f"[[Category:{c}]]", printouts)
        print(c, report["ask"][c], flush=True)
    for c in SUBOBJECT_CATEGORIES:
        report["ask"][c] = ask(out, c, f"[[Category:{c}]]", printouts + ["-Has subobject=Page"])
        print(c, report["ask"][c], flush=True)
    for ns, name in NAMESPACES.items():
        for which in ("nonredirects", "redirects"):
            folder = f"pages/{name}-{'pages' if which == 'nonredirects' else 'redirects'}"
            report["pages"][folder] = listing(out, folder, {"action": "query", "list": "allpages", "apnamespace": ns,
                                                            "apfilterredir": which, "aplimit": 500},
                                              "allpages", "apcontinue")
        for t in ("delete", "move", "merge"):
            folder = f"log/{t}-{name}"
            report["log"][folder] = listing(out, folder, {"action": "query", "list": "logevents", "letype": t,
                                                          "lenamespace": ns, "lelimit": 500,
                                                          "leprop": "ids|title|type|timestamp|details"},
                                            "logevents", "lecontinue")
        print(name, report["pages"], flush=True)
    report["finished"] = now()
    report["typed_properties"] = len(typed)
    (out / "harvest.json").write_text(json.dumps(report, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    print(json.dumps(report, indent=1))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
