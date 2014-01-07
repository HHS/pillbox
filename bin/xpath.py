# ------------------
# Pillbox Xpath script that extracts raw data from XML
# ------------------
# Requirements: Python 2.6 or greater 

import time, os, zipfile
from lxml import etree
from itertools import groupby

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
	# Set headers, to be joined later with python dictionary
	topLevelHeader = ['set_info', 'sponsors','prod_medicines','ingredients']
	setInfoHeader = ['id_root','setid','file_name','effective_time','date_created','prikey']
	sponsorsHeader = ['name','setid','prikey']
	prodMedicinesHeader = ['product_code','product_name','form_code','splcolor','splimprint','splshape','splsize','splscore','dea_schedule_code','dea_schedule_name','spl_ingredients']
	ingredientsHeader = ['pm_prikey','ingredient_type','numerator_unit','numerator_value','dominator_unit','dominator_value','substance_code','substance_name','active_moiety_names','prikey']

	#Create objects to be filled with extracted information
	setInfo = {}
	sponsors ={}
	prodMedicines = {}
	ingredients = {}

	# Iterparse function that clears the memory each time it finishes running
	def getelements(filename, tag):
		context = iter(etree.iterparse(filename, events=('start', 'end')))
		_, root = next(context) # get root element
		for event, elem in context:
			if event == 'end' and elem.tag == tag:
				yield elem
				root.clear() # preserve memory

	# ---------------
	# Build SetInfo array
	# ---------------
	setInfo['file_name'] = name
	setInfo['date_created'] = time.strftime("%d/%m/%Y")
	setInfo['prikey'] = {}
	for host in getelements(path+name, "{urn:hl7-org:v3}document"):
		for child in host.iterchildren('{urn:hl7-org:v3}id'):
			setInfo['id_root'] = child.get('root')
			child.clear()
		for child in host.iterchildren('{urn:hl7-org:v3}setId'):
			setInfo['setid'] = child.get('root')
			# Also set the id for sponsors array
			sponsors['setid'] = child.get('root')
			child.clear()
		for child in host.iterchildren('{urn:hl7-org:v3}effectiveTime'):
			setInfo['effective_time'] = child.get('value')
			child.clear()

	# ---------------
	# Build Sponsors Array
	# ---------------
	for host in getelements(path+name, "{urn:hl7-org:v3}author"):
		for x in host.iter('{urn:hl7-org:v3}representedOrganization'):
			for y in x.iterchildren('{urn:hl7-org:v3}name'):
				sponsors['name'] = y.text

	print sponsors
	print setInfo

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