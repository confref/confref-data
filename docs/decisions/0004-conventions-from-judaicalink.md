# 0004 The conventions of judaicalink-data apply

Status: accepted · Date: 2026-11-08

## Context

With the framework ([0003](0003-repository-and-framework.md)) come the conventions it was built for. Deviating only for
a good reason keeps both projects consistent.

## Decision

These decisions of judaicalink-data (<https://github.com/judaicalink/judaicalink-data/tree/main/docs/decisions>)
apply to confref as written there, with our names (confref-data, `cr`, `id.confref.org`):

| judaicalink-data | Subject |
|---|---|
| 0006 | one file = one named graph = dataset IRI; `-meta` files with provenance |
| 0007, 0024 | prefer complementary datasets; fix by new versions, corrections or complements, never by editing published files |
| 0008 | facts are stated about records and about the entity they concern |
| 0009, 0022 | entity pages: one set at a time, merges keep the oldest IRI, splits coin new ones, IRIs never reused (for confref: the identifier set `ids`, [0005](0005-identifiers.md)) |
| 0011 | generators are deterministic and independent of their earlier output |
| 0012 | everything in English |
| 0013, 0014, 0040 | catalogue format, locations and data index, pictures of entries |
| 0016, 0017 | data access is outside the data repository; slugs name the dataset |
| 0018, 0021 | the generator framework; the store and the inputs area |
| 0019, 0041 | dumps locations are equal, the git history is the permanent record; pruning |
| 0023 | correction datasets |
| 0028 | one User-Agent for every request (ours: `confref-data (https://confref.org)`) |
| 0029, 0032, 0037, 0038 | identity from our own linksets, identity declarations and measured link quality, judged linksets, facts per class |
| 0030 | Dublin Core only as `dcterms:` |
| 0033 | withdrawn datasets |
| 0035 | normalised dates: `xsd:date`/`gYearMonth`/`gYear`, else EDTF |

Not taken over (about JudaicaLink's history, hosts or sources): 0001–0005, 0010, 0015, 0020, 0025–0027, 0031,
0034, 0036, 0039.

## Consequences

A change of one of these conventions for confref is a decision here, and a deviation in
[`../judaicalink-deviations.md`](../judaicalink-deviations.md).
