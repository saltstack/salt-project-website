---
title: "saltdocker Repository Now Archived"
summary: "The Salt Project will no longer publish new containers of salt to dockerhub, and has archived the saltdocker repository. Community members can access and fork the repository if they wish to create or maintain similar containers."
date: "2024-02-01"
author: Derek Ardolf
url: "blog/saltdocker-archival"
image: images/blog/new-update.png
image_alt:
tags:
    - announcement
---

The [saltdocker](https://gitlab.com/saltstack/open/saltdocker) repo, which historically published [saltstack/salt](https://hub.docker.com/r/saltstack/salt) container images, has been archived.

In March 2023 of last year, the core Salt team updated the README to state that we do not officially support it. Prior to that time, we released new containers only if the pipeline functioned well enough. So the README was updated to reflect the official policy:

> **WARNING** These containers are not officially supported, they were initially created by the community for testing purposes and the core team only facilitates the publishing of the containers.

We haven't published new `saltdocker` containers for the `v3007.0rc0`, nor for the latest `v3006.6` and `v3005.5` Salt releases. We have no plans to release new versions of these containers in the future.

If you use these containers, and wish to continue using them, the archived repository is available for forking. Be aware that Alpine 3.14, the current container version used in `saltdocker`, is EOL and may be impacted by security vulnerabilities that will not be fixed by the core Salt team. Only use the containers if you are comfortable with those risks.