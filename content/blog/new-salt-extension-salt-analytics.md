---
title: "New Salt Extension: Salt Analytics (Salt managed data processing pipelines)"
date: 2023-04-28T22:25:54-06:00
tags:
    - salt
    - extensions
    - analytics
---

# New Salt Extension: Salt Analytics (Salt managed data processing pipelines)

**April 28, 2023 - Caleb Beard**

The Salt Project team is releasing a new salt extension, salt-analytics-framework, to allow users to run data processing pipelines alongside Salt.

These pipelines are managed by Salt as an engine and consist of the following steps:
  - Collecting (logs, run salt modules, etc...)
  - Processing (masking, etc...)
  - Forwarding (disk, etc...)

Each of these steps is pluggable, meaning you can write your own collectors, processors, and forwarders to suit whatever specific use cases that may arise. You can write a simple Python package with your plugins, and with the correct entrypoints, they will be available to use in your pipelines after your package is installed. With this pluggability, salt-analytics-framework opens the door to use machine learning models to process and analyze data.

Simple install instructions: On a salt-master system with targeted minions...

    salt <targets> pip.install salt-analytics-framework

Example: Dump memory usage and status information to disk every 5 seconds.

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

Links:
  - docs: [https://salt-analytics-framework.readthedocs.io](https://salt-analytics-framework.readthedocs.io)
  - github: [https://github.com/saltstack/salt-analytics-framework](https://github.com/saltstack/salt-analytics-framework)
  - pypi: [https://pypi.org/project/salt-analytics-framework](https://pypi.org/project/salt-analytics-framework)
