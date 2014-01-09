import os
import sys
import requests
import simplejson as json

# Uses setid and product_name from SPL

def rxNorm(ndc):
	baseurl = 'http://rxnav.nlm.nih.gov/REST/'
	
	#http://rxnav.nlm.nih.gov/REST/rxcui?idtype=NDC&id=0591-2234-10
	# Set url parameters for searching RXNorm for SETID
	ndcSearch = 'rxcui?idtype=NDC&id='
	
	# Request RXNorm API to return json 
	header = {'Accept': 'application/json'}

	# Search RXNorm using NDC code, return RXCUI id
	r = requests.get(baseurl+ndcSearch+ndc, headers=header)
	rxID = json.loads(r.text, encoding="utf-8")
	rxCUI = rxID['idGroup']['rxnormId'][0]

	return rxCUI

rxNorm('0591-2234-10')
