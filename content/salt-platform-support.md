---
title: "Salt Platform Support"
layout: "single"
url: "/salt-platform-support"
summary: Salt Platform Support
---

# Salt Platform Support

## Supported Operating Systems
Before implementing Salt to manage any data center infrastructure it is important to understand a few things about Salt platform support including: What platforms will the Salt Master run on? What systems and infrastructure can be managed by a Salt Minion? Salt runs on and manages many versions of Linux, Windows, Mac OS X and UNIX. The Salt Supported Operating System document defines the specific operating systems that are fully supported  and outlines the package creation policy for each operating system listed. The document also outlines the best-effort support policy for additional operating systems.

The Salt Support Operating System guidelines, in addition to the Salt product lifecycle phases and definitions listed below, are intended to clearly define how long a particular operating system and Salt version will receive official packages, testing, and technical support.

## Product Lifecycle
### Lifecycle Phases
| Salt Version | Phase 1 support ends | Phase 2 support ends | Phase 3 support ends | Extended life support ends |
| ------------ | -------------------- | -------------------- | -------------------- | ------------------------- |
| 3003         | Sep 30, 2021         | Mar 31, 2022         | Sep 30, 2022         | Sep 30, 2023              |
| 3002         | Apr 21, 2021         | Oct 21, 2021         | Apr 21, 2022         | Apr 21, 2023              |
| 3001         | Dec 31, 2020         | Jun 30, 2021         | Dec 31, 2021         | Dec 31, 2022              |
| 3000         | Aug 31, 2020         | Feb 28, 2021         | Aug 31, 2021         | Aug 31, 2022              |
| 2019.2       | Sep 30, 2019         | Mar 31, 2020         | Sep 30, 2020         | Sep 30, 2021              |
| 2018.3       | Oct 31, 2018         | Apr 30, 2019         | Oct 31, 2019         | Oct 31, 2020              |
| 2017.7       | Jan 31, 2018         | Jun 30, 2018         | Aug 30, 2019         | Dec 31, 2019              |
| 2016.3       | Nov 30, 2016         | May 31, 2017         | Nov 30, 2017         | Nov 30, 2018              |
| 2015.8       | Mar 31, 2016         | Sep 30, 2016         | Mar 31, 2017         | Mar 31, 2018              |
| 2015.5       | Nov 31, 2015         | May 31, 2016         | Nov 30, 2016         | Nov 30, 2017              |
| 2014.7       | May 31, 2015         | Nov 30, 2015         | May 31, 2016         | May 31, 2017              |

## Support Life Cycle Phase Definitions
### Phase 1: Regular point release support
During phase 1, Salt Project will issue regular point releases with critical bug fixes. Improved software functionality may be provided at the discretion of the project. Point releases will include the content of previously released updates. The focus of phase 1 releases will be high and critical bugs.

### Phase 2: On-demand support
During phase 2, Salt Project may release point releases with bug fixes as requested by SaltStack customers. Point releases will include the content of previously released updates. The focus of phase 2 releases will be high or critical bugs.

### Phase 3: CVE support
During phase 3, Salt Project will release point releases with fixes for selected, critical CVEs. Fixes in newer branches will not be back ported.

### Extended life support
During extended life support, Salt Project will not release any point releases. Users will still have access to any documentation. Salt Project will provide ongoing best-effort technical support for customers on existing installations. No bug fixes, security fixes, improved functionality, or root-cause analysis will be provided.

## Phase Details
| Support                                 | Phase 1 support (6 months) | Phase 2 support (6 months) | Phase 3 support (6 months) | Extended Life Support (12 months) |
| --------------------------------------- | ------------------------- | ------------------------- | ------------------------- | --------------------------------- |
| Access to existing documentation        | Yes                       | Yes                       | Yes                       | Yes                               |
| Technical support (paid subscription)   | Yes                       | Yes                       | Yes                       | Yes (Best Effort)                 |
| Access to customer portal (paid subscription) | Yes                 | Yes                       | Yes                       | Yes                               |
| CVE Fixes                               | Yes                       | Yes                       | Yes                       | —                                 |
| Point Release with bug fixes            | Yes                       | Yes                       | —                         | —                                 |
| Software Enhancements                   | Yes                       | —                         | —                         | —                                 |
