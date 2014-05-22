---
title: "Understand the Process"
layout: docs
category: docs
class: data
columns: 1
background-color: grey
link1: http://dailymed.nlm.nih.gov/dailymed/about.cfm
link1title: 'Download the Source Data'
link1info: 'Source data is available from DailyMed in XML format. DailyMed is a service of the National Library of Medicine (NLM)'
link2: https://github.com/HHS/pillbox-data-process/tree/master/scripts#pillbox-data-process
link2title: Data Processing with Python
link2info: Python scripts download the DailyMed XML files, and process them into a JSON API and CSV.
---

Pillbox's primary data source ([FDA drug labels](http://www.fda.gov/forindustry/datastandards/structuredproductlabeling/default.htm)) is complex and does not organize information based on individual pills. A Python data process is used to download the source data and produce an easy to use, "pill-focused" dataset. This improved data process is the beginning of greater flexibility for developers to understand the process and access the data.

This script can be run on your local machine by installing [Python](http://www.python.org/) and necessary requirements. Follow [this setup guide](https://github.com/HHS/pillbox-data-process/blob/master/documentation/SETUP.md) and [steps for running the scripts](https://github.com/HHS/pillbox-data-process/tree/master/scripts#pillbox-data-process) to start processing on your own machine.
