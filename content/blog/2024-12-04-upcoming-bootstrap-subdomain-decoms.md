---
title: "Upcoming bootstrap subdomain decommission"
summary: "With the migration of salt-bootstrap script download locations, to GitHub Releases, winbootstrap.saltproject.io and bootstrap.saltproject.io will be decommissioned on 2025-01-06"
date: "2024-12-04"
author: Salt Project Team
authorbio: ""
url: "blog/upcoming-bootstrap-decommission"
image: images/blog/new-update.png
tags:
    - news
    - community
---

> This is a continuation of several blog post announcements related to infrastructure migration. Can view a recent summary so far at:
>
> - [Salt Project Blog - FAQs from Salt Project Repo Migration and Open Hour](/blog/post-migration-salt-project-faqs)

Salt Project Community Members!

Since `salt-bootstrap` scripts have been available for download via GitHub Releases, this is a reminder that `winbootstrap.saltproject.io`
and `bootstrap.saltproject.io` will not be hosting the bootstrap scripts in the near future.

The original notice was for scripts no longer being available after the **end of November 2024**, but we have extended this window to
**January 6th, 2025 (2025-01-06)**.

## salt-bootstrap downloads via GitHub Releases

The target, released scripts for bootstrap are hosted here:

- Linux: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.sh
- Windows: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.ps1

`sha256` files are hosted here:

- Linux: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.sh.sha256
- Windows: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.ps1.sha256

These links dynamically update when a new release of `salt-bootstrap` occurs, always downloading the artifacts from the latest release in GitHub Releases.

For more details, reference the [salt-bootstrap README](https://github.com/saltstack/salt-bootstrap/blob/develop/README.rst).
