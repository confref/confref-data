# 0015 The website and the dumps on bart until the VMs exist

Status: accepted · Date: 2026-11-08 · Changes [0007](0007-sparql-and-hosting.md) (the website VM) and
[0002](0002-iris-and-hosts.md) (the host of the website)

## Context

[0007](0007-sparql-and-hosting.md) planned a VM of its own for the website. On 2026-11-08 the DNS of `confref.org`,
`www.confref.org` and `archive.confref.org` was moved from HdM Stuttgart to `bart` (141.19.143.20), the web server
of Kai Eckert at TH Mannheim, which already serves static sites and stable data of other projects. A static site and
a store of files need nothing more.

## Decision

- **`www.confref.org`** serves the website (confref-site), root `/home/eckert/www.confref.org/` on bart. It is the
  canonical host: the site's `baseURL` is `https://www.confref.org/`. **`confref.org`** redirects to it (301, path kept).
- **`archive.confref.org`** is a dumps location: `/store/<slug>/<version>/<path>` = `lokal/store`, root
  `/home/eckert/archive.confref.org/`; no directory listing.
- nginx config `/etc/nginx/sites-available/confref` (the version before certbot is `confref-site/deploy/nginx-confref.conf`);
  certificates from Let's Encrypt with `certbot --nginx`, renewed by the certbot timer.
- **Deployment is by hand**: the site with `confref-site/deploy/deploy.sh` (build locally, rsync), the store with
  `rsync -rtp --exclude='.*' --exclude='/tuwien-pc/' ~/lokal/confref/store/ bart:/home/eckert/archive.confref.org/store/`.
  A commit deploys nothing.
- **`tuwien-pc` is not copied** until TU Wien has given the short written OK (`PLAN-2026-11-08-setup-and-data.md`,
  section 9); then the exclude goes.
- The landing page in `project.toml` stays `https://confref.org/` (it redirects); the platform VM `labs.confref.org`
  of [0007](0007-sparql-and-hosting.md) is unchanged.

## Consequences

- The site is public before the platform exists: `id.confref.org` and `labs.confref.org` do not resolve yet.
- The dataset pages do not link the files yet ("Downloads open with the first publication"): that needs the dumps
  locations in `catalog/locations.toml` and a real `dataindex.json` (kg-commons 0014).
- If the website later moves to a VM of its own, the names move with DNS; the paths stay.
