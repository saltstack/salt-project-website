---
title: "Salt Project Package Repository (repo.saltproject.io) Migration and Guidance"
summary: "This week, packages from `repo.saltproject.io` will be migrated to `packages.broadcom.com`. This means a variety of disruptive changes are being implemented around installing, upgrading, and pinning/locking Salt."
date: "2024-10-28"
author: Salt Project Team
authorbio: ""
url: "blog/salt-project-package-repo-migration-and-guidance"
image: images/blog/new-alert.png
tags:
    - news
    - community
---

> **UPDATE (2024-10-31):** The [Salt Install Guide](https://docs.saltproject.io/salt/install-guide/en/latest/index.html) has since been updated with directions that users should reference, going forward. For more details: [Salt Project Blog - Salt Install Guide Overhaul and salt-bootstrap updates](/blog/salt-install-guide-overhaul)

> **UPDATE (2024-11-07):** A new version of `salt-bootstrap` has been released, making use of the `packages.broadcom.com` repositories. For more details: [Salt Project Blog - New salt-bootstrap release: v2024.11.07](/blog/new-salt-bootstrap-release-2024-11-07)

Salt Project Community Members!

This week, packages from `repo.saltproject.io` will be migrated to `packages.broadcom.com`. This means a variety of disruptive changes are being implemented around installing, upgrading, and pinning/locking Salt.

# Why the change?

In order to integrate with Broadcom infrastructure and policies, we are migrating off of AWS public cloud infrastructure and consolidating services used by Salt Project by **end of October 2024**.

To achieve these goals, Salt Project has been quickly needing to migrate to GitHub Pages:

- For documentation, website/blog and `salt-bootstrap` hosting
- [Salt Project Blog - Upcoming Salt Project Docs and Repo Migrations](/blog/upcoming-salt-project-docs-and-repo-migration)
- [Salt Project Blog - salt-bootstrap Breakage and Next Steps: New Updates](/blog/salt-bootstrap-breakage-part-2)

Salt Project has also needed to migrate the Salt package repository:
- `repo.saltproject.io` -> `packages.broadcom.com`: A public Artifactory endpoint for package repository hosting (rpm/deb/windows/etc.)

This also means that all self-hosted CI/CD runners, connected to our GitHub/GitLab repositories, will become non-functional when our public cloud backend is decommissioned.

# Decommissioning of Older Packages

As part of this migration, Salt Project is **dropping all packages older than Salt v3006.** This means that Salt `3005`, `3004`, etc. and older will no longer be available for installation.

**At the end of October 2024, packages will no longer be available via:**

- `repo.saltproject.io`
- `archive.repo.saltproject.io`

# Install Directions from New Package Repository

## Linux: RPM

RPM packages for Linux have been moved to:
- https://packages.broadcom.com/ui/repos/tree/General/saltproject-rpm

To prep for RPM packages of Salt:

```
curl -fsSL https://github.com/saltstack/salt-install-guide/releases/latest/download/salt.repo | sudo tee /etc/yum.repos.d/salt.repo

# Expire cache
sudo dnf clean expire-cache
```

Install (default: latest LTS version):

```
sudo dnf install salt-master
sudo dnf install salt-minion
sudo dnf install salt-ssh
sudo dnf install salt-syndic
sudo dnf install salt-cloud
sudo dnf install salt-api
```

Install a target minor version:

```
sudo dnf install salt-master-3006.9
sudo dnf install salt-minion-3006.9
sudo dnf install salt-ssh-3006.9
sudo dnf install salt-syndic-3006.9
sudo dnf install salt-cloud-3006.9
sudo dnf install salt-api-3006.9
```

Update to latest (default: latest available for 3006 LTS):

```
dnf update salt-minion
```

---

### Enable/Disable STS or LATEST Repos

```
# List available repos, and show what is enabled/disabled
dnf repolist --all salt-repo-*
```

To make 3007 STS:

```
dnf config-manager --set-disable salt-repo-*
dnf config-manager --set-enabled salt-repo-3007-sts
```

To make ALL salt packages available:

```
dnf config-manager --set-disable salt-repo-*
dnf config-manager --set-enabled salt-repo-latest
```

To ensure only 3006 LTS (default):

```
dnf config-manager --set-disable salt-repo-*
dnf config-manager --set-enabled salt-repo-3006-lts
```

---

## Linux: DEB

DEB packages for Linux have been moved to:
- https://packages.broadcom.com/ui/repos/tree/General/saltproject-deb

> **NOTE:** Since we use the same `.deb` packages across all Debian-based distros, we do not included codenames as part of the apt source list configuration.

To prep for DEB packages of Salt:

```
# Download public key
curl -fsSL https://packages.broadcom.com/artifactory/api/security/keypair/SaltProjectKey/public | sudo tee /etc/apt/keyrings/salt-archive-keyring-2023.pgp
# Create apt repo target configuration
echo "deb [signed-by=/etc/apt/keyrings/salt-archive-keyring-2023.pgp arch=amd64] https://packages.broadcom.com/artifactory/saltproject-deb/ stable main" | sudo tee /etc/apt/sources.list.d/salt.list
```

```
# Update package listings
sudo apt-get update
```

---

### Install Latest 3006 LTS

Populate `/etc/apt/preferences.d/salt-pin-1001` in order to restrict upgrades to Salt 3006.x:

```
echo 'Package: salt-*
Pin: version 3006.*
Pin-Priority: 1001' | sudo tee /etc/apt/preferences.d/salt-pin-1001
```

Install desired salt package, which will go with latest 3006 LTS version by default:

```
sudo apt-get install salt-master
sudo apt-get install salt-minion
sudo apt-get install salt-ssh
sudo apt-get install salt-syndic
sudo apt-get install salt-cloud
sudo apt-get install salt-api
```

If wanting to pin to currently installed versions:

```
sudo apt-mark hold salt-master
sudo apt-mark hold salt-minion
sudo apt-mark hold salt-ssh
sudo apt-mark hold salt-syndic
sudo apt-mark hold salt-cloud
sudo apt-mark hold salt-api
```

---

### Install Latest 3007 STS

Populate `/etc/apt/preferences.d/salt-pin-1001` in order to restrict upgrades to Salt 3007.x:

```
echo 'Package: salt-*
Pin: version 3007.*
Pin-Priority: 1001' | sudo tee /etc/apt/preferences.d/salt-pin-1001
```

Install desired salt package, which will go with latest 3007 STS version by default:

```
sudo apt-get install salt-master
sudo apt-get install salt-minion
sudo apt-get install salt-ssh
sudo apt-get install salt-syndic
sudo apt-get install salt-cloud
sudo apt-get install salt-api
```

If wanting to pin to currently installed versions:

```
sudo apt-mark hold salt-master
sudo apt-mark hold salt-minion
sudo apt-mark hold salt-ssh
sudo apt-mark hold salt-syndic
sudo apt-mark hold salt-cloud
sudo apt-mark hold salt-api
```

---

### Pin to Target Minor Version

> **NOTE:** These examples use `3006.9` for target version.

Install remaining desired packages (make sure all include `=3006.9` for target versions):

```
sudo apt-get install salt-master=3006.9
sudo apt-get install salt-minion=3006.9
sudo apt-get install salt-ssh=3006.9
sudo apt-get install salt-syndic=3006.9
sudo apt-get install salt-cloud=3006.9
sudo apt-get install salt-api=3006.9
```

> **NOTE:** If going with a non-latest point release of a target major version, you may be required to install other salt packages in a pinned fashion. For example, to install `salt-minion=3006.8`, a user will be required to install `salt-common` at the same version:
> - `sudo apt-get install salt-minion=3006.8 salt-common=3006.8`

Pin to target versions:

```
sudo apt-mark hold salt-master
sudo apt-mark hold salt-minion
sudo apt-mark hold salt-ssh
sudo apt-mark hold salt-syndic
sudo apt-mark hold salt-cloud
sudo apt-mark hold salt-api
```

---

## Windows

Installs for Windows have been moved to:

- https://packages.broadcom.com/ui/repos/tree/General/saltproject-generic/windows
- When navigating, users can find specific versions of packages. A download URL is available when clicking on a specific target.
- `sha256` values also will appear on the same page of the download URLs.

Example downloads for Salt 3006.9 LTS:

|Arch|File type|Download install file|sha256|
|--|--|--|--|
|AMD64|exe|https://packages.broadcom.com/artifactory/saltproject-generic/windows/3006.9/Salt-Minion-3006.9-Py3-AMD64-Setup.exe|2f90752b832d7f7f9bddfc2748a43ca7caa639f8f8e9b7841fff53b16c33bb81|
|AMD64|msi|https://packages.broadcom.com/artifactory/saltproject-generic/windows/3006.9/Salt-Minion-3006.9-Py3-AMD64.msi|0a6ce24aabff0149217fe9b1a9d6f63ac3136ce65d2b0e83c7d58bcf4ff6f263|
|x86|exe|https://packages.broadcom.com/artifactory/saltproject-generic/windows/3006.9/Salt-Minion-3006.9-Py3-x86-Setup.exe|e149bdf176d817b92e55c9089f3884d8cf03f66b65c71fefbeb2122e199a6f97|
|x86|msi|https://packages.broadcom.com/artifactory/saltproject-generic/windows/3006.9/Salt-Minion-3006.9-Py3-x86.msi|0ce7677f51ad373c38b1984908c422fccf2eeeff82bef2ba23ae8c4c9b4b60ce|

---

## MacOS

Installs for MacOS have been moved to:

- https://packages.broadcom.com/ui/repos/tree/General/saltproject-generic/macos
- When navigating, users can find specific versions of packages. A download URL is available when clicking on a specific target.
- `sha256` values also will appear on the same page of the download URLs.

Example downloads for Salt 3006.9 LTS:

|Arch|File type|Download install file|sha256|
|--|--|--|--|
|arm64|pkg|https://packages.broadcom.com/artifactory/saltproject-generic/macos/3006.9/salt-3006.9-py3-arm64.pkg|81fca1bcd46eed09a6f5b97451a1238a6a78a97a1af6757cf6a73b2bb7b6db6d|
|x86_64|pkg|https://packages.broadcom.com/artifactory/saltproject-generic/macos/3006.9/salt-3006.9-py3-x86_64.pkg|	5366e96e38073863522c2fc8097c97f7698a84c22f9899cbdf796b1e8b45b1e0|

# Next Steps

Salt Project will be giving an overhaul to the [Salt Install Guide directions](https://docs.saltproject.io/salt/install-guide/en/3006/) in order to reflect this new way of managing packages.

In the meantime: We request that the Salt Project community provide feedback/improvements that can be done via the [Salt Project Community Discord](https://discord.gg/J7b7EscrAs) (in the `#documentation` channel) and the [Salt Install Guide GitHub Repo](https://github.com/saltstack/salt-install-guide/).
