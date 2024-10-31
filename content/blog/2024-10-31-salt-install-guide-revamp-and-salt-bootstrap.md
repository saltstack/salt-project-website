---
title: "Salt Install Guide Overhaul and salt-bootstrap updates"
summary: "The Salt Install Guide has been updated to reflect the Salt package repository migration to packages.broadcom.com, and salt-bootstrap is non-functional as fixes to the scripts are underway."
date: "2024-10-31"
author: Salt Project Team
authorbio: ""
url: "blog/salt-install-guide-overhaul"
image: images/blog/new-alert.png
tags:
    - news
    - community
---

> This is a continuation of several blog post announcements related to infrastructure migration:
>
> - [Salt Project Blog - Upcoming Salt Project Docs and Repo Migrations](/blog/upcoming-salt-project-docs-and-repo-migration)
> - [Salt Project Blog - Salt Project Package Repository (repo.saltproject.io) Migration and Guidance](/blog/salt-project-package-repo-migration-and-guidance)
> - [Salt Project Blog - salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2)

## Salt Install Guide

[The Salt Install Guide](https://docs.saltproject.io/salt/install-guide/en/latest/) has had a gigantic overhaul in order to accurately work with `packages.broadcom.com` hosted Salt repositories, including quite a bit of simplification:

- There are no longer multiple versions of the Salt Install Guide: directions for each operating system include tabs or tables for LTS and STS installations.
- Linux directions have been reduced down to two types: RPM (RHEL-like systems) and DEB (Debian-like systems). We're able to do this because of onedir (via `relenv`), and how we've been merely duplicating a single `.deb` and `.rpm` across many repositories rather than having custom packages per target operating system.
- For pinning to major versions, or even specific minor point release versions, we now depend on built-in package manager configurations rather than providing a large collection of isolated repositories.

> **NOTE:** The install guide does still have areas of it that need updates, that have TBD placeholders, and `salt-bootstrap` is currently non-functional (see below). For issues discovered in the Salt Install Guide, open issues in the [Salt Install Guide source repo](https://github.com/saltstack/salt-install-guide/) and post in the `#documentation` channel of the [Salt Project Community Discord](https://discord.gg/J7b7EscrAs).

## salt-bootstrap

Though `salt-bootstrap` scripts expect to be [downloaded from a new location now](/blog/salt-bootstrap-breakage-part-2), the script itself no longer works as current releases don't support the new `packages.broadcom.com` repository.

A dedicated issue has been created and assigned for fixing these issues:

- [salt-bootstrap scripts broken: Need a new release to work with `packages.broadcom.com` repos](https://github.com/saltstack/salt-bootstrap/issues/2027)

We apologize for any inconvenience this may cause and appreciate your patience as we work to improve your Salt Project experience. 

-- Salt Project Team
