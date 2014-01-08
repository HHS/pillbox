import os
import sys
import requests
import simplejson as json

# Uses setid and product_name from SPL

def rxNorm(splSETID, name):
	baseurl = 'http://rxnav.nlm.nih.gov/REST/'
	
	# Set url parameters for searching RXNorm for SETID
	setidSearch = 'rxcui?idtype=SPL_SET_ID&id='
	searchOption = '&allsrc=value'
	
	# Set url parameters to matching name with RXNorm 
	check = 'rxcui/'
	checkOption = '/allProperties?prop=NAMES'
	
	# Request RXNorm API to return json 
	header = {'Accept': 'application/json'}

	r = requests.get(baseurl+setidSearch+splSETID+searchOption, headers=header)

	rxIDs = json.loads(r.text, encoding="utf-8")

	for i in rxIDs['idGroup']['rxnormId']:
		rCheck = requests.get(baseurl+check+i+checkOption, headers=header)
		checkName = json.loads(rCheck.text, encoding="utf-8")
		if checkName['propConceptGroup']['propConcept'][0]['propValue'].lower() == name.lower():
			return i
		# need to add rxtty and rxname 

# Sample data from SPL: 
# 	splSETID = 'db1311ad-9732-4fdb-80dc-95b09077e3d0'
# 	name = 'TRIAZOLAM'
rxNorm('0a4d39b0-396f-4ae0-9332-68557c6d4f74', 'Nabumetone')
