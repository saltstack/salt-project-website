## Salt Project Website

The main static site for https://saltproject.io, built with [Hugo](https://gohugo.io/).

### Install prerequisites

- [Install Hugo](https://gohugo.io/installation/)
  - Version `v0.133.0` or higher
  - This was built with the `extended` version of Hugo, but may not be required
- Git

### Build a local preview

```bash
# Serves for viewing changes locally
# Dynamically loads updates when changes happen in repo
hugo serve
```

Preview http://localhost:1313/ in your browser.

> **NOTE:** By default, this doesn't include building The Hacks episodes locally. View the sections below that are related to The Hacks for information on how to include them in a local preview.

### Contributing

TODO

#### New blog post

TODO

#### New "The Hacks" podcast episode

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

## GitLab Pages

TODO
