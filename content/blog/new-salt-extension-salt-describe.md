---
title: "New Salt Extension: Salt Describe (Automate Generating SLS files)"
date: 2023-04-27T22:25:54-06:00
---

# New Salt Extension: Salt Describe (Automate Generating SLS files)
**April 27, 2023 - Megan Wilhite**

The Salt project team is releasing a new salt extension salt-describe to create templates for Salt by fetching the settings of remote salt minions. It can create templates for:
 - users
 - files
 - packages
 - services
 - timezone data
 - iptables data
 - cron
 - sysctl
 - etc.

It will help anyone get a starter template from a system they already own with a salt minion on it. The generated templates can be used as is or edited to better suit your environment. They make a great starting place to develop formulas for your infrastructure-as-code project. This can also help to copy the settings of an existing brownstone server and deploy it to many other systems.

Simple install instructions: 

on a salt-master system with a salt-minion:

    root@salt00:/srv/salt/home# salt-pip install saltext.salt-describe
    Collecting saltext.salt-describe
        Downloading saltext.salt_describe-0.1.1-py2.py3-none-any.whl (30 kB)
    Installing collected packages: saltext.salt-describe
    Successfully installed saltext.salt-describe-0.1.1

For updated install instructions see [https://salt-describe.readthedocs.io/en/latest/gettingstarted.html](https://salt-describe.readthedocs.io/en/latest/gettingstarted.html)

Example: create Salt formula for installing all packages that the remote system lists are installed. 

    root@salt00:/srv/salt/home# salt-run describe.pkg web.example.com
    Generated SLS file locations:
        - /srv/salt/web.example.com/pkg.sls

Current describe modules include but are not limited to pkg, sysctl, cron, files, firewalld, host, iptables, pip, pkgrepo, service, timezone, users

For more info, please see the docs at:
 - https://salt-describe.readthedocs.io/en/latest/index.html

Links:
 - docs: https://salt-describe.readthedocs.io/en/latest/index.html
 - github: https://github.com/saltstack/salt-describe
 - pypi: https://pypi.org/project/saltext.salt-describe