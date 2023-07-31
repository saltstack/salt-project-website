---
title: "New Salt Extension: Salt Analytics (Salt managed data processing pipelines)"
summary: "The Salt Project team is releasing salt-analytics-framework, a new Salt extension, to allow users to run data processing pipelines alongside Salt."
date: "2023-04-28"
author: Caleb Beard
url: "blog/new-salt-extension-salt-analytics"
image: images/blog/new-extension.png
image_alt:
tags:
    - salt extensions
    - releases
---

# New Salt Extension: Salt Analytics (Salt managed data processing pipelines)

The Salt Project team is releasing **salt-analytics-framework**, a new Salt
extension, to allow users to run data processing pipelines alongside Salt.

These pipelines are managed by Salt as an engine and consist of the following
steps:
  - Collecting (logs, run salt modules, etc...)
  - Processing (masking, etc...)
  - Forwarding (disk, etc...)

Each of these steps is plugable, meaning you can write your own collectors,
processors, and forwarders to suit whatever specific use cases that may arise.
You can write a simple Python package with your plugins, and with the correct
entrypoints, they will be available to use in your pipelines after your package
is installed. With this plugability, salt-analytics-framework opens the door to
use machine learning models to process and analyze data.

Simple install instructions: On a salt-master system with targeted minions, run:

```
salt <targets> pip.install salt-analytics-framework
```
Example: Dump memory usage and status information to disk every 5 seconds.

```
    engines:
        - analytics

    beacons:
     memusage:
        - interval: 5
        - percent: 0.01%
    status:
        - interval: 5
        - time:
        - all
    loadavg:
        - all

    analytics:
    collectors:
        beacons-collector:
        plugin: beacons
        beacons:
            - "*"

    processors:
        noop-processor:
        plugin: noop

    forwarders:
        disk-forwarder:
        plugin: disk
        path: /var/cache/salt
        filename: events-dumped.txt
        pretty_print: true

    pipelines:
        my-pipeline:
        collect: beacons-collector
        process: noop-processor
        forward: disk-forwarder
```

Links:
  - Docs: [https://salt-analytics-framework.readthedocs.io](https://salt-analytics-framework.readthedocs.io)
  - GitHub: [https://github.com/saltstack/salt-analytics-framework](https://github.com/saltstack/salt-analytics-framework)
  - PyPi: [https://pypi.org/project/salt-analytics-framework](https://pypi.org/project/salt-analytics-framework)
