# openlych-docs

Documentation for OpenLych and its KDL config language. Built with
[Zensical](https://zensical.org) (the successor to Material for MkDocs),
deployed free to GitHub Pages.

## Local preview

```sh
python3 -m venv .venv && source .venv/bin/activate
pip install zensical
zensical serve          # live preview
zensical build --clean  # static output in ./site
```

## Deploy to GitHub Pages

1. Push this repo to GitHub.
2. Settings → Pages → Build and deployment → Source: **GitHub Actions**.
3. The workflow in `.github/workflows/deploy.yml` builds and deploys on every
   push to `main`.

## Structure

- `zensical.toml`: site config, nav, theme (brand pink, Inter + JetBrains Mono).
- `docs/index.md`: home page and entry points.
- `docs/getting-started.md`: install, run, first flow, debugger.
- `docs/usage/`: app-level pages (jobs, proxies, hits, settings, OpenBullet import).
- `docs/kdl/`: the KDL language reference, one page per step family.
- `docs/stylesheets/extra.css`: exact brand colour overrides.
- `docs/assets/`: logo and favicon.

The theme pins the OpenLych palette to match the app and the landing site.

## Keeping the reference honest

The KDL grammar in `docs/kdl/` mirrors `src/kdlcfg.rs` and `src/model.rs` in the
OpenLych repo: node names, keyword arguments, and operation lists come from
there. When the engine adds or renames a step, update the matching page in the
same change. The sample configs in the app's `data/configs/` are the executable
form of this reference.
