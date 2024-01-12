---
title: "Undocumented Features: Salt Runner Silence"
summary: "Runner modules have an undocumented configuration parameter that allows for enhanced control over the
output of the Runner modules."
date: "2023-12-05"
author: Nicholas M. Hughes
url: "blog/salt-runner-silence"
image: images/blog/coworkers-meeting-03.jpg
image_alt:
tags:
    - community
    - documentation
---

# Undocumented Features: Salt Runner Silence

> Nicholas Hughes is a founding partner and CEO of EITR Technologies and a champion of Salt Project. This blog entry also appears on the EITR blog at: <https://www.eitr.tech/blog/2023/11/9/undocumented-features-salt-runner-silence>

Salt Project is a useful tool for DevOps. It has functionality for days (as the
kids say), and Runner modules stand out as powerful utilities that allow for the
execution of tasks directly on the master. Runners are typically executed from
the command line using the `salt-run` command, with their output displayed in
stdout. However, a deeper exploration into the Salt Project's code base reveals
an undocumented feature that adds a layer of flexibility and security to the
execution of Runner modules.


## Unveiling the undocumented feature

Runner modules, while traditionally executed directly on the master, can also be
triggered by publishing an event on a minion through the `publish.runner`
execution module. While this method offers a different approach to executing
Runner modules, it also raises a concern: the potential exposure of sensitive
output information in the journalctl logs. This alternative execution method may
end up redirecting the output from stdout to the journalctl logs on the master
depending on the service configuration.

Addressing this concern is an undocumented configuration parameter: `quiet`.
Found within the code, this hidden gem allows for enhanced control over the
output of the Runner modules. By setting `quiet: true` in the master
configuration, the output from the execution of Runner modules is suppressed,
preventing it from being displayed in the journalctl logs. This helps in
maintaining the confidentiality of sensitive information which may be otherwise
exposed by a Runner module.

## The way forward: enhanced documentation

It's somewhat disconcerting to stumble upon an undocumented feature like the
`quiet` configuration parameter in the Salt Project's code base. When it comes
to Salt for DevOps, users and administrators rely on comprehensive documentation
to fully utilize the platform's capabilities and ensure secure and efficient
operations. Discovering features through a meticulous code base exploration,
rather than straightforward documentation, is far from ideal. However, this
discovery provides an opportunity for improvement. Ensuring that features,
especially those pertinent to security and operational efficiency, are
well-documented and easily accessible, is imperative. We'll be working on
documenting and/or creating a better workflow for this behavior, enhancing the
user experience and the overall functionality of the Salt Project. At EITR, we
love Open Source!