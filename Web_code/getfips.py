import os	
import requests
import json

def getfips(lat,lng):
	""" Returns FIPS code from latitude and longitude """
	link = "http://data.fcc.gov/api/block/find?format=json&latitude=" + str(lat) + "&longitude=" + str(lng)

	r = requests.get(link)
	myfile = r.json()
	fips = myfile['Block']['FIPS']
	return fips
