---
title: "New salt-bootstrap release: v2024.11.07"
summary: "The new salt-bootstrap release includes support for the new packages.broadcom.com endpoint."
date: "2024-11-07"
author: Salt Project Team
authorbio: ""
url: "blog/new-salt-bootstrap-release-2024-11-07"
image: images/blog/new-release.png
tags:
    - news
    - community
    - releases
---

> This is a continuation of several blog post announcements related to infrastructure migration:
>
> - [Salt Project Blog - Upcoming Salt Project Docs and Repo Migrations](/blog/upcoming-salt-project-docs-and-repo-migration)
> - [Salt Project Blog - Salt Project Package Repository (repo.saltproject.io) Migration and Guidance](/blog/salt-project-package-repo-migration-and-guidance)
> - [Salt Project Blog - salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2)
> - [Salt Project Blog - Salt Install Guide Overhaul and salt-bootstrap updates](/blog/salt-install-guide-overhaul)

Salt Project Community Members!

Today, a new version of `salt-bootstrap` has been released, **which includes updates to start making use of `packages.broadcom.com`**:

- Support for Broadcom packaging infrastructure, `packaging.broadcom.com`
- Photon OS support only for latest Salt, that is, Salt `3007.1` (problem with Photon `tdnf` support for repo file exclude parameter)
- Linux platforms only support latest major branch versions, for example: `3006.9`, `3007.1`
- Windows and MacOS support minor branch versions, for example: `3006.8`
- Future fixes for Linux minor versions of Salt will be forth-coming: [salt-bootstrap issue #2038](https://github.com/saltstack/salt-bootstrap/issues/2038)

See details on [Salt Project Blog - salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2) for where to download the latest `salt-bootstrap` scripts.

-- Salt Project Team
