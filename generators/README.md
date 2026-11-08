# Generators

One folder per dataset (`<slug>/`): `generate.py` (the data logic; the framework does versions, run records, `-meta`),
a `README.md` (what the dataset is, its sources, how it is made, its known limits), and `runs/<version>.json` (the run
record of each version, written by `./cr add-version`). Format and rules: judaicalink-data decision 0018.
