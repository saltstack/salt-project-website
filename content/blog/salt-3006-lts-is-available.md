---
title: "Salt 3006 LTS is available"
date: 2023-04-18T22:25:54-06:00
---

# Salt 3006 LTS is available

**April 18, 2023 - Alyssa Rock**

The Salt Project has just released 3006.0 of the Salt 3006 LTS. To download and install Salt 3006, see the [Salt install guide](https://docs.saltproject.io/salt/install-guide/en/latest/). To access the 3006.0 packages directly, go to the [Salt Project Package Repository](https://repo.saltproject.io/salt/py3/). 

NOTE ON UPGRADES
The GPG key for the 3006.0 release is now named: SALT-PROJECT-GPG-PUBKEY-2023. You must download the new GPG key before upgrading or your upgrade will fail.

## New LTS/STS release strategy
3006 is the first LTS release of Salt based on a new release strategy as defined in this [Salt Enhancement Proposal](https://github.com/saltstack/salt-enhancement-proposals/pull/65). Using this new release strategy, Salt Project will release one LTS (long-term support) release of Salt per year and one STS (short-term support) release each year. The LTS release will receive bug fix releases for a longer period of time than STS releases. 

The purpose of the LTS release is to provide users with a stable version of Salt for a longer period (2 years). The purpose of the STS release is to provide a feature release to users who need or prefer access to the latest features in between LTS releases.

See [Salt version support lifecycle](https://docs.saltproject.io/salt/install-guide/en/latest/topics/salt-version-support-lifecycle.html) for more information about the release strategy.

## Improvements to the test suite
In the 3006 release, the Salt Project made several improvements to the test suite that will speed up the testing process for new PRs, including changes to test decorations and the process for running local tests with Nox. These improvements will allow the core Salt team to selectively choose to run and re-run certain tests based on which tests are applicable to the pull request. These changes will speed up the contributing and pull request review process. See the [Contributing guide](https://github.com/saltstack/salt/blob/3006.x/CONTRIBUTING.rst) for more information about the new test decorators and Nox changes.