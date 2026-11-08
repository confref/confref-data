# Catalogue

One entry per dataset, `<slug>.md`: TOML front matter and a description, in the format of kg-commons
0013 (only `slug`, `title`, `author` and `license` are required). Read with `./cr list-datasets`, `./cr show-dataset
<slug>`; check with `./cr check-catalog`.

- `agents.toml`: persons (numbered, never reused) and software agents.
- `vocabulary.toml`: the values of `kind` and `method`.
- `locations.toml`: where dumps and catalogue pages are (prefixes; entries never name them).
- `link-quality.toml`: thresholds and measured quality of identity links.
