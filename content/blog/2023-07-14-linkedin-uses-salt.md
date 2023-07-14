---
title: "How LinkedIn uses Salt to support infrastructure growth"
summary: "Here at the Salt Project, we enjoyed reading this recent blog post from LinkedIn
Engineering about how their engineering team uses Salt to support their infrastructure growth."
date: "2023-07-14"
author: Alyssa Rock
url: "/blog/linkedin-uses-salt-to-support-infrastructure-growth"
image: /images/blog/person-phone-01.jpg
image_alt:
tags:
    - case study
---

# How LinkedIn uses Salt to support infrastructure growth

Here at the Salt Project, we enjoyed reading this recent blog post from LinkedIn
Engineering:
[Scaling Salt for Remote Execution to support LinkedIn Infra growth](https://engineering.linkedin.com/blog/2023/scaling-salt-for-remote-execution-to-support-linkedin-infra-grow)

We recommend that you go and read the full blog entry for yourself, but here's
some highlights:

> At LinkedIn, site engineers like to automate operational tasks at various infrastructure layers to minimize manual interventions, which can scale well and be easy to operate. Certain automations are performed via onDemand job executions.

> LinkedIn engineers have been using Salt, a Python-based, open source software, for automating tasks at various infrastructure layers for more than a decade now, due to its high performance and pluggability. Salt comes with a rich set of execution modules which can be used directly or within custom modules. It works well for tasks such as OS upgrades, auto remediation/triage of issues, application profiling, traffic shifts, firmware upgrades, switch management and more. ...

> In this post, we will share how we scaled Salt by adding layers and integrating it with LinkedIn infrastructure to achieve 10x more remote execution jobs, with more reliability than ever before.

[Continue reading](https://engineering.linkedin.com/blog/2023/scaling-salt-for-remote-execution-to-support-linkedin-infra-grow)
