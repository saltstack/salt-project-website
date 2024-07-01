# Salt Project Website

This repository is for the main static site of https://saltproject.io, built with [Hugo](https://gohugo.io/). The site is currently hosted on AWS (CloudFront/S3), and uses GitLab Pages for previewing.

## Install prerequisites

- [Install Hugo](https://gohugo.io/installation/)
  - Version `v0.133.0` or higher.
  - This was built with the `extended` version of Hugo, which is required.
- Git

### Build a local preview

```bash
# Serves for viewing changes locally
# Dynamically loads updates when changes happen in repo
hugo serve
```

Preview http://localhost:1313/ in your browser.

> **NOTE:** By default, this doesn't include building The Hacks episodes locally. View the sections below that are related to The Hacks for information on how to include them in a local preview.

The Hugo server won't display content that is marked as `draft: true` in the Markdown front matter. It also won't display content that is set to a future date. One workaround is to remove `draft: true` and set the content date for the current date.

You could also run this command to tell Hugo to build a local preview of content that is set with a future date:

```bash
hugo server --buildFuture
```

Be aware that the command `hugo server --buildDrafts` currently errors out in Salt Project and, at the time of writing, this hasn't been fixed. The only workaround is to remove `draft: true` from the front matter.


## Contributing

To contribute, create a fork of this repository. See [Using the Fork-and-Branch Git Workflow](https://blog.scottlowe.org/2015/01/27/using-fork-branch-git-workflow/) for help.

### Push the current `main` branch to the live site

To push the latest changes in the `main` branch to the live site, you need to tag the latest changes:

1. Navigate to the home directory of the repo and ensure you see the right sidebar. (You may have to widen your window to see it.)

2. On the right sidebar, click **Tags**.

3. Make a note of the latest tag name (number). For example: `v1.0.64`.

4. Click the **New tag** button.

5. In the **Tag name** field, increase the latest tag name (number) by one digit. For example: `v1.0.65`.

6. In the **Message** field, write a brief message explaining the changes you are pushing live. For example: `Add latest Open Hour notes`.

7. Click the **Create tag** button.

8. The page now displays a link to a hash for a build pipeline, such as `e18261aa`. Click this link to view the progress of the build pipeline. When the pipeline completes, the changes to the site are live.

> **NOTE:** If the pipeline fails, view the error message to see what is going wrong. Often, re-running the pipeline fixes the problem. If not, contact the SRE team for support.


### Create a new blog post

To create a new blog post:

1. Pull down the latest changes from `main` and check out a new branch.

2. Open one of the template blog posts in your browser. These files are located in the `content > blog` folder. Open the example file based on the type of blog post you want to write:

   | If you want to write this type of post... | Use this example file... |
   | ----------------------------------------- | ------------------------ |
   | Release announcement | `example-release.md` |
   | Open Hour notes | `example-open-hour.md` |
   | Generic blog entry | `example.md` |

3. Each example file contains instructions in commented out code for how to fill in the necessary Markdown front matter for that type of blog post. Follow those instructions and edit the content.

4. Build a local preview to check that the changes render properly.

5. Stage and commit your changes, then open a merge request.

6. After the pipeline for your merge request finishes building, you can preview the staged changes. Replace the placeholder text with your GitLab username:
`<https://your-GitLab-username.gitlab.io/salt-project-website/>`

  > **NOTE:** If you want to share the local preview with someone to review your changes, you must first add them as a contributor to your fork of the Salt Project repo. This is required because this repo and your fork are private, which restricts preview access.

7. After your merge request is approved, merge it in.

8. Push the current `main` branch to the live site. (See the previous section.)

### Create a new security announcement

The process for creating a new security announcement is identical to the process for creating a new blog post. The only difference is that the security announcement content is located in a different folder: `content > security-announcements` and you use the `example.md` file located in this folder.

### Create a new "The Hacks" podcast episode post

Episodes of The Hacks are not saved in this repository, but are instead dynamically generated at build time based off of the content of [The Hacks RSS feed](https://thehacks.libsyn.com/rss). This is so that all updates made via the LibSyn portal will be automatically reflected in the episodes posted to the website (ex. fixes to links, typo corrections, etc.). This means that no merge requests are required to update the website.

To publish a new episode of The Hacks to the website:

- Run the **Republish site with latest The Hacks episodes** pipeline found in [scheduled pipelines for salt-project-website](https://gitlab.com/saltstack/open/docs/salt-project-website/-/pipeline_schedules?scope=ACTIVE)
- A new pipeline should run and retrieve the latest updates to all episodes of The Hacks!

Troubleshooting:

- If URL check breaks on a new episode, the episode content may need to be updated to fix the broken URL.
- If URL check breaks on a link that is manually verified as a passing link, then re-running the pipeline may work.
- If uncertain on how to remedy, reach out to the Docs team or SRE team.

#### Updating "The Hacks" recommended episodes

- Open `config.toml`
- Update The Hacks section

```toml
[ the-hacks ]
    recommended = [
        "VR Headsets, Why Tech Won't Just Let Them Go.",
        'The Evolution of Video Games',
        'Putting the "A.I. Genie" Back In The Bottle'
    ]
```

- Submit a new merge request with the update

> **NOTE:** The values in `recommended` need to be the _exact_ title of the episodes.

#### OPTIONAL: Build local preview with The Hacks

Usually, the CI/CD pipeline should be building these out for you so there isn't a need to do so locally unless you are making modifications to either the `tools/gen-the-hacks.py` script, or the `recommended` episodes listed in `config.toml`.

The Hacks blog pages are generated with a Python script that parses the RSS feed contents.

- Install [pyenv](https://github.com/pyenv/pyenv)
  - Optionally, can just create virtualenvs with `python -m venv .venv` if your current Python version is at least 3.11.x
- Create a new virtualenv with Python 3.11.x or higher

```bash
# Example Python version install
pyenv install 3.11.4
# Example virtualenv creation
pyenv virtualenv 3.11.4 salt-project-website
pyenv activate salt-project-website

# ALTERNATIVE TO PYENV
# python -m venv .venv
# source .venv/bin/activate

which python # Should show you are using a pyenv/venv version
python --version # Should show 3.11.x or greater
which pip # Should show you are using a pyenv/venv version
pip install -r tools/requirements.txt

# Generate The Hacks .md files needed, should be very fast
rm -rf content/the-hacks/*.md
cp tools/_index.md content/the-hacks/
python tools/gen-the-hacks.py

# Serves for viewing changes locally
# Dynamically loads updates when changes happen in repo
hugo serve
```


## How Hugo works (Hugo architecture)

Hugo is a static site generator, which means it compiles the raw content (Markdown files) and uses the layout and style code to generate HTML files that can be stored on a web server.

Many times when people use Hugo, they import a theme created by someone else that is stored in the `themes` folder and referenced in the `config.toml` file, which is the configuration file for the site. Salt Project's site is using a custom, homegrown theme. (The Salt Project `config.toml` file is pretty light and small, with all the heavy lifting being done by the rest of the site architecture.)

When you're using a custom theme, it's helpful to understand about Hugo's site architecture when using a customer theme is its overall folder structure. To generate HTML pages, Hugo expects a few important folders and files:

### Content

The `content` folder contains the raw Markdown source files that contain the content for the site. The folder contains a few stand-alone Markdown files for individual pages (called "single" pages in Hugo) and sub-folders for content that is logically grouped together and displayed in similar ways, such as the blog content, security announcements, and the working group pages.

Hugo treats `index.md` pages inside a sub-folder as a "list" page, which is useful for listing the content in that folder in a landing page.

### Layouts

The `layouts` folder contains the raw HTML files that explain how Hugo should render the content when it transformed (compiled) into HTML. You can use straight HTML or you can additionally add sophisticated logic to the pages using Hugo's coding language (Go).

The `layouts` folder structure should closely mirror the `content` folder. In other words, every file or folder that appears in the `content` folder often has a corresponding file or folder in `layouts` that tells Hugo how to render that type of content. If there isn't a corresponding file or folder, Hugo uses either the default `single` or `list` HTML layout to compile the content (depending on whether the content is a single page or a list page).


### Partials

The `layouts` folder also contains an additional folder called `partials` which contain reusable "snippets" of HTML or Go that can be called into other layout files dynamically. For example, if you open the `index.html` file in the `layouts` folder, you see a big list of partials for rendering the home page. Here's an example of one partial that substitutes the HTML for the top banner:

```
<section class="video-hero">
  {{ partial "home/banner" }}
</section>
```

When Hugo compiles that content, it substitutes the HTML code from the file found in `layouts > partials > home > banner.html`:

```html
<video playsinline="" autoplay="" muted="" loop="" id="bgvid">
    <source src="{{ "video/header_Option1.mp4" | relURL }}" type="video/mp4">
</video>
<div class="video-text">
    <h1>Welcome to Salt Project</h1>
    <p>The largest, friendliest, and most active open source community in the world.</p>
    <a href="https://docs.saltproject.io/salt/install-guide/en/latest/" class="btn outline">Get Started</a>
</div>
```

The most important partials are the `head.html`, `header.html`, and `footer.html` files, which render the global HTML versions of those HTML elements for the site.

The `header.html` file contains the code for the top nav bar (global site navigation).

### Static

The `static` folder contains the CSS, Javascript, video, and image files used by the site. For example, the `images` folder has a `blog` subfolder for all the images used on the Salt Project blog.

When you reference images in these folders, you leave off the `static` part of the filepath because Hugo expects images to the stored in this root folder.

### Miscellaneous additional folders

Most of the other folders aren't being used by the Salt Project website. However, if we ever decided to convert from CSS to SASS/SCSS, those files would be stored in the `assets` folder.

### The baseof file

In the `layouts > _default` folder, there is a `baseof.html` file that defines the baseline HTML structure for all the pages on the site. This page calls the `head.html`, `header.html`, and `footer.html` partials.

### Markdown file front matter

The Markdown content includes some front matter (metadata) at the top of each file that passes important information to Hugo when it is rendering the layout. For example, the `example.md` blog file includes this font matter:

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
    - releases
    - news
    - community
---
```

That front matter metadata sends important information that Hugo uses when building the page by swapping in the title for the blog, the summary of the blog that appears on the blog index page, the author, and so forth.

Depending on the type of content, it may need different front matter. You can view the front matter for other Markdown content files in that folder to understand what kind of front matter is needed. You can also view the layout file for that type of content to better understand how Hugo is using that front matter to render the final HTML pages.

### For deeper learning

To learn more about Hugo custom themes and site architecture, check out the free [Giraffe Academy Hugo course](https://www.giraffeacademy.com/static-site-generators/hugo/). It's a pretty helpful video guide.