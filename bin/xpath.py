# ------------------
# Pillbox Xpath script that extracts raw data from XML
# ------------------
# Requirements: Python 2.6 or greater 

import time, csv, json,  os, copy, re, sys, urllib, zipfile
from lxml import etree
from itertools import groupby
from datetime import datetime

# ------------------
# Define Functions
# ------------------

def unZipFiles(file_name):
	filePath = ('download/'+file_name).rstrip()
	fileFolder = filePath.strip('.zip')
	# Make folder for each pill to store unzipped contents, but commented out because 
	# this breaks if file already exists
	#os.makedirs(fileFolder)
	fh = open(filePath, 'rb')
	z = zipfile.ZipFile(fh)
	for name in z.namelist():
		outpath =  fileFolder + '/'
		z.extract(name, outpath)
		# Send only XML files to parseData() function
		if ".xml" in name:
			parseData(outpath, name)
	fh.close()

def parseData(path, name):
	# Get XML
	context = iter(etree.iterparse(path+name,tag='author'))
	# Loop through each IATI activity in the XML
	# Not working yet
	# for x, y in context:
	# 	print x, y

# ------------------
# Run Functions
# ------------------

# Get list of latest files added
latest = open('download/files_added.txt', 'r')

# Create array of latest file names
newFiles = []
for x in latest:
	newFiles.append(x)

# Run the starting function, only on first file for now
unZipFiles(newFiles[0])