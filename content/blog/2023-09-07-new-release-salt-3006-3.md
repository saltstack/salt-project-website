---
title: "Salt 3006.3 is available"
summary: "The Salt Project has just released the 3006.3 bugfix of the Salt 3006 LTS."
date: "2023-09-07T06:00:00"
author: Alyssa Rock
url: "blog/salt-3006-3-release-is-now-available"
image: images/blog/new-release.png
image_alt:
tags:
    - releases
---

# Salt 3006.3 is available

The Salt Project has just released the 3006.3 bugfix of the Salt 3006 LTS. To
download and install Salt 3006.3, see the
[Salt install guide](https://docs.saltproject.io/salt/install-guide/en/latest/).
To access the 3006.3 packages directly, go to the
[Salt Project Package Repository](https://repo.saltproject.io/salt/py3/).

- Release notes can be found here: https://docs.saltproject.io/en/latest/topics/releases/3006.3.html
- Changelogs can be found here: https://github.com/saltstack/salt/blob/v3006.3/CHANGELOG.md
- Sources are available on PyPI here: https://pypi.org/project/salt/3006.3/

| **IMPORTANT** |
| ------------- |
| Due to a known issue with the newest release of setuptools, users who use pip to install Salt will experience an install failure. This issue also impacts pip installs for older versions of Salt. The core Salt team is currently investigating the issue and has documented a workaround. To follow the issue and get the latest workaround, see: <https://github.com/saltstack/salt/issues/65149> |