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
				grandChild.clear()

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
	info['SPL_INGREDIENTS'] = []

	ingredient = {}
	ingredient['active'] = []
	ingredient['inactive'] = []
	
	ingredientTwo = {}
	
	for parent in getelements(path+name, "{urn:hl7-org:v3}manufacturedProduct"):
		count = count + 1
		print count, 'manufactured products'
		# First set of child elements in <manufacturedProduct> used for Ingredients
		for child in parent.iterchildren('{urn:hl7-org:v3}ingredient'):
			# Create temporary object for each ingredient
			ingredientTemp = {}
			if child.get('classCode') == 'ACTIB' or child.get('classCode') == 'ACTIM':
				ingredientTemp['active_moiety_names'] = []
				# Create object for active ingredient, for PROD_MEDICINES
				active = {}
				for grandChild in child.iterchildren('{urn:hl7-org:v3}ingredientSubstance'):
					for c in grandChild.iterchildren():
						ingredientTemp['ingredient_type'] = 'active'
						if c.tag == '{urn:hl7-org:v3}name':
							active['name'] = c.text
							ingredientTemp['substance_name'] = c.text
						if c.tag == '{urn:hl7-org:v3}code':
							active['code'] = c.get('code')
							ingredientTemp['substance_code'] = c.get('code')
						# Send active moiety to ingredientTemp
						if c.tag =='{urn:hl7-org:v3}activeMoiety':
							print 'hey!'
							name = c.find('.//{urn:hl7-org:v3}name')
							ingredientTemp['active_moiety_names'].append(name.text)

				# Send 'active' object to 'active' array
				ingredient['active'].append(active)
			
			if child.get('classCode') == 'IACT':
				# Create object for each inactive ingredient
				inactive = {}
				for grandChild in child.iterchildren('{urn:hl7-org:v3}ingredientSubstance'):
					for c in grandChild.iterchildren():
						ingredientTemp['ingredient_type'] = 'inactive'
						if c.tag == '{urn:hl7-org:v3}name':
							inactive['name'] = c.text
							ingredientTemp['substance_name'] = c.text
						if c.tag == '{urn:hl7-org:v3}code':
							inactive['code'] = c.get('code')
							ingredientTemp['substance_code'] = c.get('code')
				# Send 'inactive' object to 'inactive' array
				ingredient['inactive'].append(inactive)

			for grandChild in child.iterchildren('{urn:hl7-org:v3}quantity'):
				numerator = grandChild.find('./{urn:hl7-org:v3}numerator')
				denominator = grandChild.find('./{urn:hl7-org:v3}denominator')

				ingredientTemp['numerator_unit'] = numerator.get('unit')
				ingredientTemp['numerator_value'] = numerator.get('value')
				ingredientTemp['dominator_unit'] = denominator.get('unit')
				ingredientTemp['dominator_value'] = denominator.get('value')

			# Append temporary object to ingredients array
			ingredients.append(ingredientTemp)

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

		# Send to info object
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

	info['SPL_INGREDIENTS'].append(ingredient)
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
