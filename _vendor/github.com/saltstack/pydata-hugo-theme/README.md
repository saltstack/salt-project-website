# pydata-hugo-theme

A [Hugo Module](https://gohugo.io/hugo-modules/) port of the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/en/stable/) for use with static/documentation sites built with [Hugo](https://gohugo.io/).

**[Documentation](https://saltstack.github.io/pydata-hugo-theme/)** — feature-by-feature coverage of every option, built from `docs/` in this repo (which itself just uses the theme, no custom templates).

## Credit / Attribution

This project is an **unofficial, community-maintained port** of the PyData Sphinx Theme's design, layout, and CSS to Hugo. It is not affiliated with, endorsed by, or maintained by the PyData team.

All credit for the original design, styling, and UX of this theme goes to the PyData Sphinx Theme authors and contributors:

- Website: https://pydata-sphinx-theme.readthedocs.io/en/stable/
- Source: https://github.com/pydata/pydata-sphinx-theme

Please refer to upstream for the canonical Sphinx implementation. This repository only reimplements the theme's templates and behavior for Hugo's templating system; the vendored CSS (`static/styles/pydata-sphinx-theme.css`) is adapted directly from the upstream project.

## Usage

Add this module to your site's `hugo.toml`:

```toml
[module]
  [[module.imports]]
    path = "github.com/saltstack/pydata-hugo-theme"
```

Then run:

```sh
hugo mod get github.com/saltstack/pydata-hugo-theme
npm install   # fetches FontAwesome / Bootstrap JS mounted by the module
```

See `exampleSite/` in this repository for a minimal working site, and the `[params]` defaults in `hugo.toml` for the full set of theme options (navbar/sidebar/footer slots, logo, search, icon links, etc.) that a consuming site can override.

### Vendoring (optional, recommended)

By default, Hugo resolves this module (and its FontAwesome/Bootstrap npm mounts) at build time, which means every build needs Go and network access. If you'd rather have a fully offline, reproducible build — no Go toolchain, no npm, no live fetch — run:

```sh
hugo mod vendor
```

This copies the resolved module into your site's `_vendor/` directory, which you check into your own repo; Hugo will then always build from that local copy instead of re-resolving the module. One gotcha: `hugo mod vendor` only copies Hugo-relevant files (`layouts/`, `static/`, `hugo.toml`, etc.) — it skips this module's own `LICENSE`/`README.md`, so re-copy those manually into `_vendor/.../pydata-hugo-theme/` after vendoring (and again after every re-vendor) if you want the attribution notice to travel with the vendored copy.

To keep this from becoming a manual chore, wrap the update in a small script that bumps the module, re-vendors, and re-copies those two files — see [`salt-project-website`'s `scripts/update-vendored-theme.sh`](https://github.com/saltstack/salt-project-website/blob/main/scripts/update-vendored-theme.sh) for a reference implementation you can adapt (it's specific to that repo's layout, so isn't shipped as part of this module).

## Contributing

`docs/` is this theme's own documentation site — it resolves the theme via a local `replace => ../` in `docs/go.mod`, so it's always in sync with whatever's currently in `layouts/`/`hugo.toml`, live, with no vendoring step:

```sh
cd docs && hugo server
```

Edit any file under `docs/content/` (or the theme's own `layouts/`/`hugo.toml`) and the running server picks it up immediately. It deploys to GitHub Pages automatically on every push to `main` via `.github/workflows/docs.yml`.

## License

BSD 3-Clause. See [LICENSE](./LICENSE). As with the code itself, the license terms mirror the upstream PyData Sphinx Theme's BSD 3-Clause license.
