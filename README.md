# Salt Project Website

This repository is for the main static site of https://saltproject.io, built with [Hugo](https://gohugo.io/) using a custom Hugo port of the [PyData Sphinx Theme](https://pydata-sphinx-theme.readthedocs.io/) (vendored in `themes/pydata`). The site is built and deployed to **GitHub Pages** via GitHub Actions.

## Install prerequisites

- [Install Hugo](https://gohugo.io/installation/)
  - Version `v0.135.0` or higher (this is the version pinned in CI — see `.github/workflows/gh-pages.yml`).
  - This was built with the `extended` version of Hugo, which is required.
- Git
- Python 3.14+ (only needed to run `scripts/validate-tags.py` locally)

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
   | Release announcement | `example-release.md` |
   | Open Hour notes | `example-open-hour.md` |
   | Generic blog entry (including security advisories) | `example.md` |

3. Each example file contains instructions in commented out code for how to fill in the necessary Markdown front matter for that type of blog post. Follow those instructions and edit the content.

   The page title is rendered automatically from the front matter `title` field — don't add a duplicate `# Title` heading at the top of the body.

4. Build a local preview to check that the changes render properly.

5. Stage and commit your changes, then open a pull request against `main`.

6. Once the `PR checks` workflow passes and the PR is approved, merge it in.

7. Push the current `main` branch to the live site by cutting a new release. (See [Push the current `main` branch to the live site](#push-the-current-main-branch-to-the-live-site).)

### Create a new security announcement

Security advisories are no longer a separate content type — they're just blog posts tagged `security`, published in `content/blog` alongside everything else, as part of a single unified blog feed. Follow the same process as [Create a new blog post](#create-a-new-blog-post) and use the `security` tag.

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

This site uses a custom theme — a Hugo port of the PyData Sphinx Theme — vendored under `themes/pydata` and referenced by the `theme` key in `hugo.toml` (Hugo's configuration file). The theme is tracked directly in this repository, so it can be edited like any other part of the site.

### Content

The `content` folder contains the raw Markdown source files that contain the content for the site. It's organized into a few sections:

- `content/blog` — the unified blog feed: release announcements, community updates, Open Hour notes, and security advisories, all tagged appropriately (see [Blog post tags](#blog-post-tags)).
- `content/community` — standalone community pages (event calendar, working groups, RSS feeds).
- `content/security-announcements` — kept only for the legacy `/security-announcements/` RSS feed URL (see [Create a new security announcement](#create-a-new-security-announcement)); it no longer holds its own post content.

Hugo treats `_index.md` pages inside a folder as a "list" page, which is useful for listing the content in that folder on a landing page.

### Layouts

The `layouts` folder contains the raw HTML files that explain how Hugo should render content when it's transformed (compiled) into HTML, using Hugo's templating language (Go templates).

Most of the site's layout logic lives in the theme (`themes/pydata/layouts`). The top-level `layouts` folder holds project-specific overrides and additions that go beyond (or intentionally diverge from) the theme's defaults — for example:

- `layouts/page.html` — overrides the theme's default page template to automatically render the page title as an `<h1>`, so individual pages don't need a duplicate Markdown heading.
- `layouts/community/event-calendar.html` and `layouts/community/working-groups.html` — custom layouts for those two community pages, selected via the `layout` front matter field on their respective content files.

When Hugo looks for a template, it checks the project's `layouts` folder first and falls back to the theme's `layouts` folder if there's no project-level override. This means the theme can be updated/upstreamed while site-specific customizations stay isolated in the top-level `layouts` folder — only touch files under `themes/pydata` directly when the fix belongs in the theme itself (e.g. a genuine theme bug), not when it's a site-specific behavior change.

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

`themes/pydata/layouts/baseof.html` defines the baseline HTML structure for all pages on the site. It calls the `head.html`, `header.html`, and `footer.html` partials, and defines the `main` block that individual page layouts fill in.

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
- `scripts/duplicate-security-feed.sh` — copies the built `tags/security` RSS feed to the legacy `/security-announcements/` URL after a Hugo build.

### GitHub Actions workflows

- `.github/workflows/pr-checks.yml` — runs on every pull request; builds the site with Hugo and validates blog post tags.
- `.github/workflows/gh-pages.yml` — builds the site on every push, and deploys it to GitHub Pages when the push is a tag matching `v**` (see [Push the current `main` branch to the live site](#push-the-current-main-branch-to-the-live-site)).

## Credits

The `themes/pydata` theme vendored in this repository is a Hugo port of the [PyData Sphinx Theme](https://github.com/pydata/pydata-sphinx-theme) ([docs](https://pydata-sphinx-theme.readthedocs.io/en/stable/)), originally built for Sphinx documentation sites. Credit to the PyData Sphinx Theme authors and contributors for the design and functionality this port is based on.

