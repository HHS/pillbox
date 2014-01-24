---
title: "Data Processing"
layout: docs
category: docs
class: data
columns: 1
link1: http://dailymed.nlm.nih.gov/dailymed/about.cfm?CFID=183228258&CFTOKEN=8603a4114605f21e-15BB5AE8-E978-A377-63D39868B9AC4364&jsessionid=8430e2cae8a7eec20716624e742245d703b7
link1title: 'Download the Data'
link1info: 'Source data is downloaded from DailyMed in XML format, which provides data on marketed drugs. DailyMed is a service of the National Library of Medicine (NLM)'
link2: https://github.com/developmentseed/pillbox/tree/master/bin
link2title: Data Processing with Python
link2info: Python scripts download the DailyMed XML files, and process them into the JSON API and CSV. 
---

Python is used to download the XML files from DailyMed, process the appropriate information from all files into the JSON API, which enables sorting by characteristic. 

This script can be run on your local machine by installing [Python](http://www.python.org/). Follow [this tutorial](https://github.com/developmentseed/pillbox-data-api/wiki/_pages) to get the process running on your own machine, or visit the links to the right to walk through the current data process.