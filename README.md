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

## Before publishing

- Set `site_url`, `repo_url`, and `repo_name` in `zensical.toml` to the real
  URLs.

## Structure

- `zensical.toml` - site config, nav, theme (brand pink, Inter + JetBrains Mono).
- `docs/` - Markdown pages. KDL reference lives in `docs/kdl/`.
- `docs/stylesheets/extra.css` - exact brand colour overrides.
- `docs/assets/` - logo and favicon.

The theme pins the OpenLych palette to match the app and the landing site.
