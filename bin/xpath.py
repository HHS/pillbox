# ------------------
# Pillbox Xpath script that extracts raw data from XML
# ------------------
# Requirements: Python 2.6 or greater 

import time, os, zipfile
from lxml import etree
from itertools import groupby


# ------------------
# Define Variables
# ------------------

# Set headers, to be joined later with python dictionary
topLevelHeader = ['set_info', 'sponsors','prod_medicines','ingredients']
setInfoHeader = ['id_root','setid','file_name','effective_time','date_created','prikey']
sponsorsHeader = ['name','setid','prikey']
prodMedicinesHeader = ['product_code','product_name','form_code','splcolor','splimprint','splshape','splsize','splscore','dea_schedule_code','dea_schedule_name','spl_ingredients']
ingredientsHeader = ['pm_prikey','ingredient_type','numerator_unit','numerator_value','dominator_unit','dominator_value','substance_code','substance_name','active_moiety_names','prikey']

#Create objects to be filled with extracted information
setInfo = {}
sponsors ={}
prodMedicines = []
ingredients = []

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
	for parent in getelements(path+name, "{urn:hl7-org:v3}document"):
		for child in parent.iterchildren('{urn:hl7-org:v3}id'):
			setInfo['id_root'] = child.get('root')
			child.clear()
		for child in parent.iterchildren('{urn:hl7-org:v3}setId'):
			setInfo['setid'] = child.get('root')
			# Also set the id for sponsors array
			sponsors['setid'] = child.get('root')
			child.clear()
		for child in parent.iterchildren('{urn:hl7-org:v3}effectiveTime'):
			setInfo['effective_time'] = child.get('value')
			child.clear()

	# --------------------
	# Build Sponsors Array
	# --------------------
	for parent in getelements(path+name, "{urn:hl7-org:v3}author"):
		for child in parent.iter('{urn:hl7-org:v3}representedOrganization'):
			for grandChild in child.iterchildren('{urn:hl7-org:v3}name'):
				sponsors['name'] = grandChild.text

	# -------------------------
	# Build ProdMedicine and Ingredients arrays
	# -------------------------
	count = 0
	info = {}
	formCodes = []
	codes = []
	formCodes = []
	names = []
	info['SPLCOLOR']  = []
	info['SPLIMPRINT'] = []
	info['SPLSHAPE'] = []
	info['SPLSIZE'] = []
	info['SPLSCORE']  = []
	info['SPLFLAVOR']  = []

	for parent in getelements(path+name, "{urn:hl7-org:v3}manufacturedProduct"):
		
		count = count + 1
		print count, 'manufactured products'
		print '________________________________________________'
		print
		# First set of child elements in <manufacturedProduct> used for Ingredients
		# for child in parent.iterchildren('{urn:hl7-org:v3}ingredient'):
		# 	ingredient = {}
		# 	for grandChild in child.iterchildren():
		# 		ingredient['pm_prikey'] = {}
		# 		ingredient['type'] = grandChild.get('classCode')
		# 	ingredients.append(ingredient)

		# To do: Abstract the three for loops below into a function
		for child in parent.iterchildren('{urn:hl7-org:v3}code'):
			if child.get('code') not in codes:
				codes.append(child.get('code'))

		for child in parent.iterchildren('{urn:hl7-org:v3}name'):
			if child.text not in names:
				names.append(child.text)

		for child in parent.iterchildren('{urn:hl7-org:v3}formCode'):
			if child.get('code') not in formCodes:
				formCodes.append(child.get('code'))

		# Append to info object
		info['product_code'] = codes
		info['product_name'] = names
		info['form_code'] = formCodes

		# Second set of child elements in <manufacturedProduct> used for ProdMedicines array
		def checkForValues(type, grandChild):
			print "Added", type
			if type == 'SPLIMPRINT':
				value = grandChild.find("./{urn:hl7-org:v3}value").text
			else:
				value = grandChild.find("./{urn:hl7-org:v3}value").attrib
			kind = grandChild.find("./{urn:hl7-org:v3}code[@code='"+type+"']")
			if kind !=None:
				if type == 'SPLIMPRINT':
					if value not in info[type]:
						info[type].append(value)
				elif type == 'SPLSCORE':
					if value.get('value') not in info[type]:
						info[type].append(value.get('code') or value.get('value'))
				else:
					if value.get('code') not in info[type]:
						info[type].append(value.get('code') or value.get('value'))

		counts = 0
		for child in parent.iterchildren('{urn:hl7-org:v3}subjectOf'):
			for grandChild in child.findall("{urn:hl7-org:v3}characteristic"):
				# for o in grandChild.findall('./{urn:hl7-org:v3}code'):
				for each in grandChild.iterchildren('{urn:hl7-org:v3}code'):
					counts = counts + 1
					# Run each type through the CheckForValues() function
					type = each.get('code')
					checkForValues(type, grandChild)
					each.clear() #clear memory
				grandChild.clear() #clear memory	

		# for x in host.iter('{urn:hl7-org:v3}representedOrganization'):
		# 	for y in x.iterchildren('{urn:hl7-org:v3}name'):
		# 		sponsors['name'] = y.text

	prodMedicines.append(info)
	print
	print '--------------- products ----------------'
	print sponsors
	print '-----'
	print setInfo
	print '-----'
	print prodMedicines
	print '-----'
	print ingredients

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
unZipFiles(newFiles[6])