---
title: "FAQs from Salt Project Repo Migration"
summary: "With the Salt Project repo migration, in October, there have been several questions from community members. The Salt Project Team addresses several of them here."
date: "2024-11-21"
author: Salt Project Team
authorbio: ""
url: "blog/post-migration-salt-project-faqs"
image: images/blog/new-update.png
tags:
    - news
    - community
---

> This is a continuation of several blog post announcements related to infrastructure migration:
>
> - [Salt Project Blog - Upcoming Salt Project Docs and Repo Migrations](/blog/upcoming-salt-project-docs-and-repo-migration)
> - [Salt Project Blog - Salt Project Package Repository (repo.saltproject.io) Migration and Guidance](/blog/salt-project-package-repo-migration-and-guidance)
> - [Salt Project Blog - salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2)
> - [Salt Project Blog - Salt Install Guide Overhaul and salt-bootstrap updates](/blog/salt-install-guide-overhaul)
> - [Salt Project Blog - New salt-bootstrap release: v2024.11.07](/blog/new-salt-bootstrap-release-2024-11-07)

Salt Project Community Members!

There have been a lot of changes with Salt Project over the past month, due to migrations out of cloud hosting. We'd like to address a lot of questions related to the migrations.

## Short Notification Window for Disruptive Changes

Salt Project OSS core maintainers are part of the Tanzu Division, at Broadcom, along with the [Tanzu Salt (Enterprise Product)](https://www.vmware.com/products/app-platform/tanzu-salt) developers. Tanzu Division initiatives brought about many cost-saving decisions across all teams, which included the infrastructure backing Salt Project OSS in AWS.

Note that these decisions were not specifically about Salt Project OSS, but were about the entire Tanzu Division.

Working a tight timeframe, the Salt Project team needed to work with our AWS accounts being deleted without having an alternative public cloud backend. We also could not use any new, third-party platforms that would incur new cost.

With this, we quickly prioritized:

- Needing to ensure that our domains, and DNS configurations, were migrated out of AWS.
- Needing to ensure the Salt Project repository was made available, via different hosting: the solution was to host on `packages.broadcom.com`, and to have packages available via manual installation (at a minimum).
- Needing to ensure the website (this blog) and Salt docs were made available, via different hosting: the solution was GitHub Pages.
- We'd have to temporarily sacrifice our CI/CD pipeline functionality, to focus on the above goals, as they were going to completely break from the migration.

Given this short timeframe, as soon as we confirmed what we knew was going to change, we sent our first communication out:

- [Salt Project Blog - Upcoming Salt Project Docs and Repo Migrations](/blog/upcoming-salt-project-docs-and-repo-migration)

From there, the blog posts since then have documented the changes as they were implemented. The notices given to the community were directly related to the timeframe, notices, and clarifications given internally to the Salt Project Team.

## New Salt Repositories

`repo.saltproject.io` and `archive.repo.saltproject.io` no longer exist.

The new repositories are hosted on `packages.broadcom.com` at:

- Linux (RPM): [saltproject-rpm](https://packages.broadcom.com/artifactory/saltproject-rpm/)
- Linux (DEB): [saltproject-deb](https://packages.broadcom.com/artifactory/saltproject-deb/)
- GENERIC (Windows, MacOS, etc.): [saltproject-generic](https://packages.broadcom.com/artifactory/saltproject-generic)

### Layout Changes

Major layout changes in our new repositories have greatly simplified our package management.

We were only creating a single set of `deb` and `rpm` packages each release, before duplicating the packages across several directory layouts to mirror our supported operating systems. This was because of tech debt, as older packages of Salt required packages specific to each operating system before making use of `relenv` (onedir).

Instead of duplicating these packages, we now provide generic instructions for `deb` and `rpm` based package managers to install our packages.

The initial migration did not include a `filelists.xml` file in the `saltproject-rpm` repo, which prevented tools such as `foreman` from creating local mirrors. This has since been resolved via:

- [Unable to create local mirror of saltstack repo, due to filelists.xml not being available
(#67032)](https://github.com/saltstack/salt/issues/67032)

### Unsupported Versions of Salt Dropped

With these new changes, all versions of Salt prior to Salt v3006 LTS are no longer available. The unsupported packages of Salt were not included in the migration, and will not be included in the future.

> _**NOTE:** Salt `rpm` and `deb` packages will likely work on unsupported operating systems (ex. RHEL 7, etc.). This would mean that systems can run updated/patched versions of Salt instead of needing to stay on EOL versions that have security issues. With this being said, the Salt Project Team will not work on any issues opened for unsupported operating systems unless the user has reproduced the bug on a supported operating system._

### TurtleTraction Shoutout

Salt Project gives a special thanks to **TurtleTraction** for helping the Salt Project community by making mirrors of the old repositories publicly available:

- https://repo.saltproject.io.turtletraction.com/
- https://archive.repo.saltproject.io.turtletraction.com/

> _**NOTE:** These repositories are not officially provided by Broadcom or Salt Project. They are provided by TurtleTraction (a third-party). Please handle with care and avoid pointing a large number of Salt Minions to the repositories, as TurtleTraction is hosting these endpoints themselves to assist with this transition period for Salt users._

To learn more about TurtleTraction, along with their news about these mirrors, visit [the TurtleTraction website](https://www.turtletraction.com/).

### AAAA records / IPv6 support

For users of Salt with IPv6-only infrastructure, attempting to download packages from `packages.broadcom.com` will fail as the endpoint only supports IPv4 at the moment.

The Salt Project Team does not have control over this like we did back when we maintained the AWS infrastructure hosting our packages. We've reached out to the Broadcom team that manages this.

The issue is currently being tracked here:

- [packages.broadcom.com has no AAAA record / IPv6 support (#67051)](https://github.com/saltstack/salt/issues/67051)

### Salt Install Guide overhaul

Several updates and clarifications were made to the Salt Install Guide after migrating it to be hosted on GitHub Pages:

- [Repo mirroring / air-gap environment directions](https://docs.saltproject.io/salt/install-guide/en/latest/topics/other-install-types/air-gap-install.html): `rclone` and `wget` examples are provided for syncing copies of the new repositories.
- Linux install directions have been greatly simplified: Since we only provide a single set of `deb` and `rpm` packages per release, we now only provide package-specific install directions.
  - [Install Salt on Linux (DEB)](https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/linux-deb.html)
  - [Install Salt on Linux (RPM)](https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/linux-rpm.html)
- [Support for Python versions](https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-python-version-support.html): Clarification has been made that Salt Project fully supports our packaged versions of Salt, and the Python version included via `relenv` (currently Python v3.10.x).
[Salt version support lifecycle](https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-version-support-lifecycle.html): Details updates to the current Salt LTS and STS releases.
  - Salt v3006 LTS will have active support until the Salt v3008 LTS release, with CVE support for one year after initial Salt v3008 LTS release.
  - Salt v3007 STS will hit complete EOL at Salt v3008 LTS release.

## Salt Supported Operating Systems

For the most up-to-date list of supported operating systems by Salt Project, visit the [Salt Install Guide - Salt supported operating systems](https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-supported-operating-systems.html).

Some clarifications we'd like to make:

- **MacOS Support**: Salt Project will continue to test and built Salt packages on MacOS. _**These packages will not be signed, for the time being.**_
- **Amazon Linux 2 / Amazon Linux 2023 Support**: Salt Project will continue to test against these operating systems in CI/CD, and consider them to be supported by LTS and STS releases.

## salt-bootstrap status

- [A New salt-bootstrap release (v2024.11.07)](/blog/new-salt-bootstrap-release-2024-11-07) came out earlier this month, with some caveats. Further updates are underway via [salt-bootstrap issue #2038](https://github.com/saltstack/salt-bootstrap/issues/2038)
- `bootstrap.saltproject.io` and `winbootstrap.saltproject.io` endpoints are to be dropped by **end of November 2024**. Going forward, use the new GitHub Release download endpoints detailed in [salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2)
