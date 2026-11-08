# Process: from development to the catalogue and the dumps locations

The process of the framework (kg-commons 0018, 0021), with the confref names:

1. **Inputs** that are not published (archives, harvests, files from partners) go to the inputs area
   (`../lokal/inputs/<source>/<name>/` with `input.toml`): `./cr add-input`, `./cr check-inputs`.
2. **A generator** per dataset in `generators/<slug>/generate.py` holds only the data logic; `./cr generate <slug>`
   makes a run in the build area. Runs are compared with earlier versions on the canonical form
   (`./cr compare`).
3. **A version**: `./cr add-version <slug>/<run-id>` writes header comments, the `-meta` file, the run record, the
   catalogue entry and puts the files into the store (`../lokal/store/<slug>/<version>/<path>`).
   `./cr check-catalog --store --complete` must pass.
4. **Publishing** (dumps on confref.org and labs.confref.org, loading into Fuseki, Zenodo) only after the OK of Kai
   Eckert ([0001](decisions/0001-what-confref-is.md)).

Fixes follow kg-commons 0024: a systematic error of a dataset → a new version of it; single findings →
correction datasets; new facts → complements.
