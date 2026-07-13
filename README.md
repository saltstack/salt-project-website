# Salt Project Website

This repository is for the main static site of https://saltproject.io, built with [Hugo](https://gohugo.io/) using [`pydata-hugo-theme`](https://github.com/saltstack/pydata-hugo-theme), a generic Hugo port of the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/), consumed as a [Hugo Module](https://gohugo.io/hugo-modules/). The site is built and deployed to **GitHub Pages** via GitHub Actions.

## Install prerequisites

- [Install Hugo](https://gohugo.io/installation/)
  - The exact version pinned for this project is tracked in the root `.hugo-version` file. The devcontainer and CI both install that exact version automatically (see `.devcontainer/Dockerfile` and `.github/actions/setup-hugo`), so it only needs to be updated in one place.
  - Must be the `extended` version, and at least the minimum declared in the theme module's `hugo.toml` (`module.hugoVersion.min`).
- Git
- Python 3.14+ (only needed to run `scripts/validate-tags.py` locally)
- Go — version pinned in the root `.go-version` file. Only needed if you're updating the vendored theme module (see [The theme module](#the-theme-module)); not required for a normal build/serve.

No Go toolchain and no Node/npm install are required to build or serve this site: the theme module and its build-time JS dependencies (FontAwesome/Bootstrap) are vendored in `_vendor/` and checked into this repository (see [The theme module](#the-theme-module) below), so `hugo` resolves everything from disk.

### Build a local preview

```bash
# Serves for viewing changes locally
# Dynamically loads updates when changes happen in repo
hugo serve
```

Preview http://localhost:1313/ in your browser.

The Hugo server won't display content that is marked as `draft: true` in the Markdown front matter. It also won't display content that is set to a future date. One workaround is to remove `draft: true` and set the content date for the current date.

You could also run this command to tell Hugo to build a local preview of content that is set with a future date:

```bash
hugo server --buildFuture
```

Be aware that the command `hugo server --buildDrafts` currently errors out in Salt Project and, at the time of writing, this hasn't been fixed. The only workaround is to remove `draft: true` from the front matter.

## Contributing

To contribute, create a fork of this repository. See [Using the Fork-and-Branch Git Workflow](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/) for help.

Every pull request runs through the `PR checks` GitHub Actions workflow (`.github/workflows/pr-checks.yml`), which:

- Builds the site with `hugo --minify` to catch any build breakage.
- Runs `scripts/validate-tags.py` to make sure every blog post only uses tags from the approved taxonomy (see [Blog post tags](#blog-post-tags) below).

Both checks must pass before a pull request can be merged.

### Push the current `main` branch to the live site

The site deploys via the `Deploy Hugo site to Pages` GitHub Actions workflow (`.github/workflows/gh-pages.yml`). It builds on every push, but only **deploys** to GitHub Pages when the push is a tag matching `v**`.

The easiest and preferred way to cut a release is to create a **GitHub Release**, which automatically creates and pushes the underlying tag for you:

1. Merge your changes into `main` first — the tag should point at the commit you want live.

2. On GitHub, go to the repo's **Releases** page and click **Draft a new release**.

3. Under **Choose a tag**, type a new tag name following the existing convention: `v<major>.<minor>.<patch>` (e.g. the current latest tag is `v2.0.38`, so the next one would be `v2.0.39`). Select **Create new tag: \<tag\> on publish**.

4. Set **Target** to `main`.

5. Give the release a title and describe the changes being shipped (this doubles as your release notes).

6. Click **Publish release**. This pushes the new tag, which triggers the `Deploy Hugo site to Pages` workflow and publishes the changes live.

7. Watch the workflow run under the **Actions** tab to confirm the build and deploy succeed.

> **NOTE:** If the workflow fails, check the run's logs to see what's going wrong. If you can't resolve it, contact the SRE team for support.

> Alternatively, you can push a tag directly with `git tag v2.0.39 && git push origin v2.0.39`, but creating a GitHub Release is preferred since it keeps a human-readable changelog tied to each deployed tag.

### Create a new blog post

To create a new blog post:

1. Pull down the latest changes from `main` and check out a new branch.

2. Open one of the template blog posts in your browser. These files are located in the `content/blog` folder. Open the example file based on the type of blog post you want to write:

   | If you want to write this type of post... | Use this example file... |
   | ----------------------------------------- | ------------------------ |
   | Release, release candidate, or security/CVE advisory | Use `scripts/new-blog-post.py` instead — see [Generate a release, RC, or security post](#generate-a-release-rc-or-security-post) |
   | Open Hour notes | `example-open-hour.md` |
   | Generic blog entry / announcement | `example.md` |

3. Each example file contains instructions in commented out code for how to fill in the necessary Markdown front matter for that type of blog post. Follow those instructions and edit the content.

   The page title is rendered automatically from the front matter `title` field — don't add a duplicate `# Title` heading at the top of the body.

4. Build a local preview to check that the changes render properly.

5. Stage and commit your changes, then open a pull request against `main`.

6. Once the `PR checks` workflow passes and the PR is approved, merge it in.

7. Push the current `main` branch to the live site by cutting a new release. (See [Push the current `main` branch to the live site](#push-the-current-main-branch-to-the-live-site).)

### Generate a release, RC, or security post

`scripts/new-blog-post.py` generates a new, fully-populated blog post file
for the three most common (and most repetitive) post types, so you don't
have to hand-copy the closest prior post:

```bash
# New GA release (one or more versions)
python3 scripts/new-blog-post.py release --version 3008.2
python3 scripts/new-blog-post.py release --version 3008.0 --version 3006.25

# New release candidate (one version, one RC number)
python3 scripts/new-blog-post.py rc --version 3008 --rc 1

# New security/CVE advisory (one or more versions)
python3 scripts/new-blog-post.py security --version 3008.2
python3 scripts/new-blog-post.py security --version 3006.12 --version 3007.4

# General news/announcement post
python3 scripts/new-blog-post.py announcement \
  --title "Some announcement" --summary "..." --tags community
```

Each Salt major version's release track (`LTS`, `STS`, or `RC`) is looked up
in `scripts/releases.toml` — **add a new major version there before**
generating a `release`, `rc`, or `security` post for it; the script exits
with an error otherwise (`error: major version 'XXXX' not found in
scripts/releases.toml — add it before generating this post.`).

`release` and `security` are also checked against `scripts/release-log.toml`
— a log of every version ever announced (version, blog post URL, and
publish date), pre-populated from this repo's existing blog post history.
A version that's already in the log is rejected as a duplicate, and a new
version must be the next expected patch number for its major line (e.g.
if `3006.27` is the latest logged `3006.x` release, the next one must be
`3006.28` — `3006.29` or re-announcing `3006.27` are both rejected). A
major version with no prior log entries (e.g. the first release of a new
major) is allowed unconditionally. On success, the new version(s) are
appended to the log automatically — **you don't edit this file by hand**
except to fix a pre-population mistake.

Notes:
- All generated posts default to `draft: true` (pass `--publish` to skip
  that). Remove `draft: true` yourself when you're ready to ship it, same
  as any hand-written post.
- `release`/`rc`/`security` bodies are fully populated boilerplate — no
  further edits should be needed beyond removing `draft: true`.
- `security` posts are the exception: the script only scaffolds the
  wrapper text and one placeholder `### CVE-{YYYY}-{NNNNN}` block (with
  `{Description}`/`{Impact}`/`{Severity Rating}`/etc. placeholders) under
  `## CVE Details` — duplicate and fill that block in by hand per real CVE
  before publishing. The generator can't infer CVE-specific details from a
  version number alone.
- `announcement`'s `--tags` must come from the approved taxonomy in
  `scripts/tags.toml` (same validation `scripts/validate-tags.py` runs) —
  the script rejects unapproved tags immediately.

### Create a new security announcement

Security advisories are no longer a separate content type — they're just blog posts tagged `security`, published in `content/blog` alongside everything else, as part of a single unified blog feed. Use `scripts/new-blog-post.py security` (see above), or follow the same manual process as [Create a new blog post](#create-a-new-blog-post) and use the `security` tag.

The legacy `/security-announcements/` RSS feed URL is preserved for old subscribers: `scripts/duplicate-security-feed.sh` copies the built `tags/security` RSS feed to that legacy path. This runs automatically as part of the deploy workflow after the Hugo build — see `.github/workflows/gh-pages.yml`.

### Blog post tags

Every blog post's tags must come from the approved taxonomy defined in `scripts/tags.toml`. If you need to add or remove an approved tag, edit that file — no code changes required.

You can check your local posts against the taxonomy at any time with:

```bash
python3 scripts/validate-tags.py
```

This same check runs automatically on every pull request via the `PR checks` workflow.

## How Hugo works (Hugo architecture)

Hugo is a static site generator, which means it compiles the raw content (Markdown files) and uses the layout and style code to generate HTML files that can be stored on a web server.

This site uses `pydata-hugo-theme` — a generic Hugo port of the PyData Sphinx Theme — imported as a [Hugo Module](https://gohugo.io/hugo-modules/) via `[module.imports]` in `hugo.toml`. See [The theme module](#the-theme-module) for how that module is resolved in this repo.

### Content

The `content` folder contains the raw Markdown source files that contain the content for the site. It's organized into a few sections:

- `content/blog` — the unified blog feed: release announcements, community updates, Open Hour notes, and security advisories, all tagged appropriately (see [Blog post tags](#blog-post-tags)).
- `content/community` — standalone community pages (event calendar, working groups, RSS feeds).
- `content/security-announcements` — kept only for the legacy `/security-announcements/` RSS feed URL (see [Create a new security announcement](#create-a-new-security-announcement)); it no longer holds its own post content.

Hugo treats `_index.md` pages inside a folder as a "list" page, which is useful for listing the content in that folder on a landing page.

### Layouts

The `layouts` folder contains the raw HTML files that explain how Hugo should render content when it's transformed (compiled) into HTML, using Hugo's templating language (Go templates).

Most of the site's layout logic lives in the theme module (`_vendor/github.com/saltstack/pydata-hugo-theme/layouts`). The top-level `layouts` folder holds project-specific overrides and additions that go beyond (or intentionally diverge from) the theme's defaults — for example:

- `layouts/page.html` — overrides the theme's default page template to automatically render the page title as an `<h1>`, so individual pages don't need a duplicate Markdown heading.
- `layouts/community/event-calendar.html` and `layouts/community/working-groups.html` — custom layouts for those two community pages, selected via the `layout` front matter field on their respective content files.

When Hugo looks for a template, it checks the project's `layouts` folder first and falls back to the theme module's `layouts` folder if there's no project-level override. This means the theme can be updated/upstreamed while site-specific customizations stay isolated in the top-level `layouts` folder — a fix that belongs in the theme itself (e.g. a genuine theme bug or a generically useful option) should be made in the `pydata-hugo-theme` module's own repository, not by editing the vendored copy under `_vendor/` directly (those edits are overwritten the next time the module is re-vendored).

### Partials

Both the theme and the project's `layouts` folder can contain a `_partials` folder with reusable "snippets" of HTML/Go template code that get called into other layout files dynamically, for example:

```
{{ partial "header-article.html" . }}
```

The most important partials are `head.html`, `header.html`, and `footer.html`, which render the global HTML for those elements across the site.

### Static

The `static` folder contains CSS, JavaScript, and other static assets that are copied as-is into the built site. `static/images` holds site images (for example, `static/images/blog` for blog post images).

When you reference these files in content or templates, you leave off the `static` part of the path, since Hugo serves everything under `static` from the site root.

### The baseof file

`_vendor/github.com/saltstack/pydata-hugo-theme/layouts/baseof.html` defines the baseline HTML structure for all pages on the site. It calls the `head.html`, `header.html`, and `footer.html` partials, and defines the `main` block that individual page layouts fill in.

### Markdown file front matter

The Markdown content includes some front matter (metadata) at the top of each file that passes important information to Hugo when it is rendering the layout. For example, a blog post's front matter looks like:

```
---
draft: true
title: "Title"
summary: "Summary"
date: "yyyy-mm-dd"
author: Testy McTester - DELETE IF ANONYMOUS
authorbio: "Author bio here. Delete if no bio."
url: "blog/title-shortened"
image: images/blog/
image_alt:
tags:
    - release
    - community
---
```

That front matter metadata sends important information that Hugo uses when building the page — swapping in the title, the summary that appears on the blog index page, the author, and so on.

Depending on the type of content, it may need different front matter. See the example files in `content/blog` (`example.md`, `example-release.md`, `example-open-hour.md`) to understand what front matter is needed for each type of post.

### Scripts

The `scripts` folder holds standalone helper scripts used in local development and CI:

- `scripts/validate-tags.py` — validates blog post tags against the approved taxonomy in `scripts/tags.toml`.
- `scripts/new-blog-post.py` — generates a new release, RC, security, or announcement blog post (see [Generate a release, RC, or security post](#generate-a-release-rc-or-security-post)). Release track lookups come from `scripts/releases.toml`; duplicate/sequence checks and history come from `scripts/release-log.toml`.
- `scripts/_blog_common.py` — small shared helper module (`scripts/tags.toml`/`scripts/releases.toml`/`scripts/release-log.toml` loaders) used by both `validate-tags.py` and `new-blog-post.py`.
- `scripts/duplicate-security-feed.sh` — copies the built `tags/security` RSS feed to the legacy `/security-announcements/` URL after a Hugo build.

### GitHub Actions workflows

- `.github/workflows/pr-checks.yml` — runs on every pull request; builds the site with Hugo and validates blog post tags. Only ever requests `contents: read` — see the security note at the top of `gh-pages.yml` for why it must stay that way.
- `.github/workflows/gh-pages.yml` — builds the site on every push, and deploys it to GitHub Pages when the push is a tag matching `v**` (see [Push the current `main` branch to the live site](#push-the-current-main-branch-to-the-live-site)). Deploy-time (`pages`/`id-token` write) permissions are scoped to just the `deploy` job; it never triggers on `pull_request`.
- `.github/workflows/check-theme-updates.yml` — runs weekly (and on-demand via `workflow_dispatch`) to check for a newer `pydata-hugo-theme` module release; opens a PR if `scripts/update-vendored-theme.sh` finds changes to vendor. Never triggers on `pull_request`, since it needs `contents: write`/`pull-requests: write` to open that PR.
- `.github/actions/setup-hugo` — local composite action shared by the workflows above to install the Hugo CLI. Defaults to the version pinned in the root `.hugo-version` file — the same file the devcontainer's `Dockerfile` reads — so the required Hugo version only needs to be maintained in that one place.

### The theme module

`pydata-hugo-theme` is a standalone, generic Hugo Module — it carries no Salt Project branding or content, so it can be reused by any Hugo site. This repo consumes it via `[[module.imports]]` in `hugo.toml` and a `require`/`replace` pair in the root `go.mod`.

The module (including its FontAwesome/Bootstrap build-time JS, mounted via `[[module.mounts]]` in the module's own `hugo.toml`) is checked into this repo under `_vendor/github.com/saltstack/pydata-hugo-theme/` via `hugo mod vendor`. This means:

- No Go toolchain, npm, or network access is needed to build or serve this site — `hugo` reads everything it needs straight out of `_vendor/`.
- `_vendor/` is **generated** — never hand-edit files under it. To pick up a theme change, run:

  ```bash
  scripts/update-vendored-theme.sh          # update to the latest module version
  scripts/update-vendored-theme.sh v0.2.0   # or pin a specific version
  ```

  This bumps the module (`hugo mod get`), re-vendors it (`hugo mod vendor`), and re-copies `LICENSE`/`README.md` — the two non-Hugo files `hugo mod vendor` doesn't carry over — into `_vendor/github.com/saltstack/pydata-hugo-theme/`. Review the resulting diff, then commit it.

  A scheduled GitHub Actions workflow (`.github/workflows/check-theme-updates.yml`) runs this same script weekly and opens a PR if anything changed, so updates don't rely on someone remembering to check. It can also be run on demand from the **Actions** tab (`workflow_dispatch`). Either way, updates are never auto-merged — re-vendoring the theme stays a deliberate, human-reviewed action.

- Their license text isn't duplicated anywhere else in this repo — see `_vendor/github.com/saltstack/pydata-hugo-theme/LICENSE`.

## Credits

`pydata-hugo-theme` is a Hugo port of the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme) ([docs](https://pydata-sphinx-theme.readthedocs.io/en/stable/)), originally built for Sphinx documentation sites. Credit to the PyData Sphinx Theme authors and contributors for the design and functionality this port is based on. See the module's own `README.md` (`_vendor/github.com/saltstack/pydata-hugo-theme/README.md`) for the full attribution notice.

## License

This repository as a whole is **not** released under an open source or Creative Commons license — all rights reserved except as noted below.

The one exception is the vendored `pydata-hugo-theme` module: it is licensed under the **BSD 3-Clause License**, matching the license used by the upstream [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme). See `_vendor/github.com/saltstack/pydata-hugo-theme/LICENSE` for the full text.

