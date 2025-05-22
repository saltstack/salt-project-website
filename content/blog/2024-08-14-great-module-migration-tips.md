---
title: "The Great Salt Module Migration"
summary: "In Salt 3008 Argon, many states and modules that you might be currently using will be migrated to extensions because of the Great Module Migration."
date: "2024-08-21"
author: Max Arnold
authorbio: "Author of https://salt.tips and active Salt Project Community contributor"
url: "blog/the-great-salt-module-migration/"
canonicalUrl: https://salt.tips/the-great-salt-module-migration/
image: images/blog/coworkers-meeting-08.jpg
tags:
    - news
    - community
---

In Salt 3008 Argon, many states and modules that you might be currently using will be gone:

* Salt 3008 release is currently scheduled for the autumn of 2024
* Around 750 modules will no longer be shipped with Salt
* Only ~100 of them (as of the time of the writing) were migrated to various Salt extensions
* Other modules are stored in a separate [holding repository](https://github.com/salt-extensions/community-extensions-holding/)
* To check whether a module was migrated, type its name into the [search box (on the Salt Tips blog version of this post)](https://salt.tips/the-great-salt-module-migration/#search-box)

## Salt extensions history

Have no idea what Salt extensions are? Roughly speaking, an extension is a Python package containing various kinds of Salt modules that can be installed via `salt-pip` or `pip.installed`. Below is a little bit of historical context:

* They were introduced in [February 2016](https://github.com/saltstack/salt/pull/31218) and released in Salt 2016.9 (I can't even find the corresponding release notes)
* A major improvement was added in November 2020 and released in [Salt 3003](https://salt.tips/whats-new-in-salt-aluminium-release#salt-extensions)
* In July 2022, Tom Hatch submitted a [SEP](https://github.com/saltstack/salt-enhancement-proposals/blob/24660626d9fe26953cd4581be0804ddfd0ceeb90/extention-migration.md) to migrate lots of built-in modules to extensions
* In October 2023, a [project board](https://github.com/orgs/salt-extensions/projects/5/views/1) was created to track the migration process
* After the Broadcom event, the push really came to shove, and it looks like there [won't be any deprecation period](https://www.youtube.com/watch?v=CubGR8rTy3Y&t=1452s)
* In January 2024, the [list of modules to be extracted](https://github.com/saltstack/great-module-migration) was opened for comments. Take your time to read it. Note that there will be three kinds of modules - core, extended core and community.
* The modules are being migrated into the [salt-extensions](https://github.com/salt-extensions) community org
* In February 2024, the [great module purge PR](https://github.com/saltstack/salt/pull/65971) was created
* In April 2024, the great module purge PR was merged, making 3008 the target release

## What can you do about it?

### Disable Salt auto updates

It is a good idea to disable automatic Salt master and minion package updates. You do not want them to update to 3008 on their own without your approval.

### Inspect your Salt state tree

You can get a rough list of used state modules (assuming they are included in the `top.sls` file) using the following one-liner:

```
salt minion1 state.show_lowstate --out json | jq -r '.[][].state' | sort -u
```

If that is too cryptic and cumbersome to remember, install the [TSL module](https://gitlab.com/turtletraction-oss/saltext-tsl) by running `sudo salt-pip install saltext.tsl` on a minion and then try the following command on your state tree:

```
sudo salt-call tsl.states
```

To see which SLS files use a particular state function, run another command:

```
sudo salt-call tsl.state file.managed
```

### Identify other kinds of modules you use

That could be: execution modules (often called via Jinja or CLI), external pillar, grains, cloud, beacons, engines, runners, sdb, returners, executors, fileservers, proxy, serializers, renderers, outputters, roster, etc. This could be done by inspecting master and minion config files, your runbooks, shell scripts, etc.

### Identify which modules were moved to extensions

You can do that using the [search box](https://salt.tips/the-great-salt-module-migration/#search-box), and it will show the corresponding Salt extensions if they exist. Alternatively, skim through the [great module purge PR](https://github.com/saltstack/salt/pull/65971) and look for the corresponding extensions in the [salt-extensions](https://github.com/salt-extensions) community org.

### Start testing Salt 3008

You can try the [nightly builds](https://repo.saltproject.io/salt-dev/master/) or wait till 3008 Release Candidate. To install an extension into a Salt Master or Minion onedir environment, use [`salt-pip` or `pip.installed`](https://docs.saltproject.io/salt/install-guide/en/3007/topics/install-dependencies.html).

### If an extension does not exist

The quick and dirty way is to grab a removed module from the [holding repository](https://github.com/salt-extensions/community-extensions-holding/), drop it into your Salt state tree (into `_modules`, `_states`, etc.) and sync via `saltutil.sync_all`. But this method is not a long-term solution.

A better way is to convert a module (or a set of related modules) into a Salt extension:

1. Watch the [Salt Extension Overview](https://www.youtube.com/watch?v=hhomJkwxK3Q) video
2. Check out the [Create and Maintain Salt Extensions Guide](https://salt-extensions.github.io/salt-extension-copier/) created by Salt Community members.
3. Create and publish your extension using the [salt-extension-copier](https://github.com/salt-extensions/salt-extension-copier) template (the original [salt-extension](https://github.com/saltstack/salt-extension) template mentioned in the overview video is deprecated)
4. It is highly advised to publish your extension repository under the [salt-extensions](https://github.com/salt-extensions) umbrella for better discoverability
5. Join the [#salt-extensions](https://discord.com/invite/J7b7EscrAs) Discord channel if you want to discuss something first or have any questions. There are also regular Salt Extensions [WG meetings](https://saltproject.io/calendar/) ([*.ics](https://calendar.google.com/calendar/ical/salt.project%40broadcom.com/public/basic.ics) link) you can attend.

> **For more information regarding The Great Module Migration, and all things Salt,  be sure to check Max Arnold’s [Salt Tips](https://salt.tips/the-great-salt-module-migration/) website\!**
