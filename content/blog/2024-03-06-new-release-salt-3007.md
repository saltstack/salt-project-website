---
title: "Salt 3007.0 STS is available"
summary: "The Salt Project has just released Salt 3007 STS."
date: "2024-03-06"
url: "blog/salt-release-3007-is-now-available"
image: images/blog/new-release.png
tags:
    - releases
---

The Salt Project has just released 3007 STS of Salt. To download and
install Salt 3007.0, see the
[Salt install guide](https://docs.saltproject.io/salt/install-guide/en/latest/).
To access the 3007.0 packages directly, go to the
[Salt Project Package Repository](https://repo.saltproject.io/salt/py3/).

- Release notes can be found here: https://docs.saltproject.io/en/latest/topics/releases/3007.0.html
- Changelogs can be found here: https://github.com/saltstack/salt/blob/v3007.0/CHANGELOG.md
- Sources are available on PyPI here: https://pypi.org/project/salt/3007.0/

## Master cluster ability

This release adds the ability to create a cluster of masters that run behind a load balancer.

For more information:

- [Master cluster page](https://github.com/saltstack/salt/blob/3007.x/doc/topics/tutorials/master-cluster.rst)
- [Master cluster SEP](https://github.com/saltstack/salt-enhancement-proposals/blob/1433501a1417f78c895345a675e21a8b6382bb61/0000-master-cluster.md)


## TCP mTLS and WebSocket transports

One benefit of WebSocket over TCP is the ability of smarter routing of requests with load balancers that support TLS termination and routing based on headers. For instance, you could have both request server and publish server behind a load balancer that is listening on 443.


## Vault refactoring

In this release, the Vault integration has been rewritten while also retaining backward compatibility. This rewrite of Vault now provides higher-level abstractions to interact with Vault.


Thank you all for your contributions!