---
title: "salt-bootstrap Breakage and Next Steps"
summary: "salt-bootstrap downloads via curl will need to be modified, as existing curl calls against bootstrap.saltproject.io and winbootstrap.saltproject.io no longer work. Read for details on how to resolve this issue."
date: "2024-10-25"
author: Salt Project Team
authorbio: ""
url: "blog/salt-bootstrap-breakage"
image: images/blog/new-alert.png
tags:
    - news
    - community
---

> **UPDATE (2024-10-29):** By end of **November 2024**, we will no longer be using the `bootstrap.saltproject.io` and `winbootstrap.saltproject.io` subdomains. Instead, users will be downloading bootstrap scripts directly from GitHub Releases. For more details: [salt-bootstrap Breakage and Next Steps: Part 2](/blog/salt-bootstrap-breakage-part-2)

> **UPDATE (2024-10-31):** The `salt-bootstrap` scripts themselves don't currently work with the new `packages.broadcom.com` repositories. For more details: [Salt Install Guide Overhaul and salt-bootstrap updates](/blog/salt-install-guide-overhaul)

> **UPDATE (2024-11-07):** A new version of `salt-bootstrap` has been released, making use of the `packages.broadcom.com` repositories. For more details: [Salt Project Blog - New salt-bootstrap release: v2024.11.07](/blog/new-salt-bootstrap-release-2024-11-07)

Salt Project Community Members!

Due to DNS migrations, there has been an unexpected breakage with downloading of the `salt-bootstrap` script.

## salt-bootstrap breakage of script download

Attempting to download the `salt-bootstrap` script no longer works by using the originally expected approach (ex. `curl -L https://bootstrap.saltproject.io`).

Due to the scripts now being hosted via GitHub Pages, website hosting is limited to static sites without custom configuration for HTTP redirect status codes. This means that our static sites are using HTML meta refresh redirects, which are unsupported by the `curl -L` command.

This means that **ALL scripts and tooling that include pulling down Salt bootstrap from `https://bootstrap.saltproject.io` or `https://winbootstrap.saltproject.io` directly, without subpaths, will fail.**

## salt-bootstrap solution

The target scripts for bootstrap are hosted here:

- Linux: https://bootstrap.saltproject.io/bootstrap-salt.sh
- Windows: https://winbootstrap.saltproject.io/bootstrap-salt.ps1

`sha256` files are hosted here:

- Linux: https://bootstrap.saltproject.io/bootstrap-salt.sh.sha256
- Windows: https://winbootstrap.saltproject.io/bootstrap-salt.ps1.sha256

### Downloading for Linux

```
# Linux
curl -o bootstrap-salt.sh -L https://bootstrap.saltproject.io/bootstrap-salt.sh
```

### Downloading for Windows

```
# Windows
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Tls12'
Invoke-WebRequest -Uri https://winbootstrap.saltproject.io/bootstrap-salt.ps1 -OutFile "$env:TEMP\bootstrap-salt.ps1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
& "$env:TEMP\bootstrap-salt.ps1"
```

## Next Steps

We are in the process of updating documentation to reflect the needed changes and updates, **as we will not be able to revert to previous functionality.**

We apologize for any inconvenience this may cause and appreciate your patience as we work to improve your Salt Project experience. 

-- Salt Project Team
