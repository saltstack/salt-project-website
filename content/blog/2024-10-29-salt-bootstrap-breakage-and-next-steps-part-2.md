---
title: "salt-bootstrap Breakage and Next Steps: New Updates"
summary: "salt-bootstrap downloads via curl will need to be modified, as salt-bootstrap scripts will need to be downloaded from GitHub Releases instead. Read for details on how to resolve this issue."
date: "2024-10-29"
author: Salt Project Team
authorbio: ""
url: "blog/salt-bootstrap-breakage-part-2"
image: images/blog/new-alert.png
tags:
    - news
    - community
---

> **UPDATE (2024-10-31):** This article details how to download the `salt-bootstrap` scripts from a new location, but the `salt-bootstrap` scripts themselves don't currently work with the new `packages.broadcom.com` repositories. For more details: [Salt Install Guide Overhaul and salt-bootstrap updates](/blog/salt-install-guide-overhaul)

Salt Project Community Members!

Due to DNS and infrastructure migrations, there was an unexpected breakage with downloading of the `salt-bootstrap` script.

Details about this were originally shared in [salt-bootstrap Breakage and Next Steps](/blog/salt-bootstrap-breakage), but the initial remedy is not sustainable in the long-term due to the nature of GitHub Pages hosting and rate limiting. With this in mind, Salt Project will be using links to GitHub releases instead of `bootstrap.saltproject.io` and `winbootstrap.saltproject.io` subdomains.

**The subdomain approach to downloading the bootstrap script, the method referenced in the above blog post, will be deprecated by end of November 2024. If that method is used throughout the month, users may experience degraded behavior later in the month due to monthly rate limits.**

## salt-bootstrap solution: GitHub Releases

The target, released scripts for bootstrap are hosted here:

- Linux: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.sh
- Windows: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.ps1

`sha256` files are hosted here:

- Linux: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.sh.sha256
- Windows: https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.ps1.sha256

These links dynamically update when a new release of `salt-bootstrap` occurs, always downloading the artifacts from the latest release in GitHub Releases.

### Downloading for Linux

```
# Linux
curl -o bootstrap-salt.sh -L https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.sh
```

### Downloading for Windows

```
# Windows
[System.Net.ServicePointManager]::SecurityProtocol = [System.Net.SecurityProtocolType]'Tls12'
Invoke-WebRequest -Uri https://github.com/saltstack/salt-bootstrap/releases/latest/download/bootstrap-salt.ps1 -OutFile "$env:TEMP\bootstrap-salt.ps1"
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
& "$env:TEMP\bootstrap-salt.ps1"
```

## Next Steps

We are in the process of updating documentation to reflect the needed changes and updates, **as we will not be able to revert to previous functionalities.**

We apologize for any inconvenience this may cause and appreciate your patience as we work to improve your Salt Project experience. 

-- Salt Project Team
