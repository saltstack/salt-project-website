---
title: "Upcoming Salt Project Docs and Repo Migrations"
summary: "Salt Project is migrating off of the current backends used for hosting saltproject.io, docs.saltproject.io, and repo.saltproject.io"
date: "2024-10-23"
author: Salt Project Team
authorbio: ""
url: "blog/upcoming-salt-project-docs-and-repo-migration"
image: images/blog/new-alert.png
tags:
    - news
    - community
---

Salt Project Community Members!

We've been working on migrating and simplifying the infrastructure behind Salt Project, which we have mentioned in the previous Salt Project Open Hour. Over the next two weeks, some major changes will be implemented.

## Salt Project: Blog and Docs

We will be migrating our backend to GitHub Pages for hosting Salt Project documentation and the main blog website. This change will affect the following websites:

- https://saltproject.io
- https://docs.saltproject.io

The migration is planned for **Friday, October 25th, 2024 (2024-10-25)**.

During the DNS propagation and cutover, users may experience connection quirks. We apologize for any inconvenience this may cause and appreciate your patience as we work to improve your Salt Project experience. We expect that the change will be barely noticeable to users.

## Salt Project: Package Repository

We are also planning a migration of the Salt Project repository by end of October 2024. This change will affect the following:

- Current location: https://repo.saltproject.io
- Future location: https://packages.broadcom.com

Upon migration, Salt Project will be deprecating `repo.saltproject.io`, **which will mean a breaking change in scripts and installation automation expecting to pull from or install packages from `repo.saltproject.io` in your infrastructure.**

More communications will come out in the next few days on the timeline, and how the Salt Install Guide will be updating to reflect the new repo location.

-- Salt Project Team
