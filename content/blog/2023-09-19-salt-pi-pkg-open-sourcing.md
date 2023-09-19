---
title: "Salt Project is Open Sourcing salt-pi-pkg"
summary: "Salt Project is open sourcing salt-pi-pkg build script examples for classic packages on Raspberry Pi."
date: "2023-09-19"
author: Derek Ardolf
url: "blog/salt-pi-pkg-open-source/"
image: images/blog/new-update.png
image_alt:
tags:
    - announcement
---

# Salt Project is Open Sourcing salt-pi-pkg

Salt Project is open sourcing [salt-pi-pkg](https://github.com/vmware-archive/salt-pi-pkg/tree/main) build script examples for classic packages on Raspberry Pi.

## What is salt-pi-pkg?

Salt Project / VMware has ended active development of salt builds for `armhf` architecture (pre-arm64/aarch64 builds of `salt`), and will receive no future updates.

`salt-pi-pkg` is an unsupported, unmaintained repository of example scripts for building "classic" (non-Tiamat, non-onedir, pre-3006.x) packages for `armhf` Raspberry Pi systems.

Scripts exist for the following OS versions:

- Raspbian 10 (armhf / 32-bit)
- Raspbian 11 (armhf / 32-bit)

## Why make these scripts available?

Salt Project is open sourcing these scripts as a follow-up to [Salt Project announcing the open sourcing of several Salt Project Native Minions]({{< ref "/2022-07-12-salt-native-minion-open-sourcing" >}} "Salt Project Announces the Open Sourcing of Several SaltStack Native Minions").

These are example scripts referenced when previously building `armhf` Raspbian packages for Raspberry Pi devices, and some users may still want to build packages themselves in order to have newer versions of Salt, such as Salt v3005.2.

- If using `arm64` Raspbian OS (64-bit OS on Raspberry Pi 3 and newer Pi devices), `arm64` LTS/STS [onedir-based builds](https://docs.saltproject.io/salt/install-guide/en/latest/topics/upgrade-to-onedir.html#what-is-onedir) would be a better alternative:
  - [Debian Install Directions](https://docs.saltproject.io/salt/install-guide/en/latest/topics/install-by-operating-system/debian.html)
  - Debian 10 arm64 example repo directory base path: https://repo.saltproject.io/salt/py3/debian/10/arm64/
  - Debian 11 arm64 example repo directory base path: https://repo.saltproject.io/salt/py3/debian/11/arm64/
