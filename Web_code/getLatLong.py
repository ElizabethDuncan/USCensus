import os
import requests
import json

def getLatLong(cityName):
	""" Returns longitude and latitude of any entered city/address queried from Google's 
	geocoding API """

	API_key = "AIzaSyBPXmopy8R-l6RdY8PdAicBGy18YWT-Dm8"


	link = "https://maps.googleapis.com/maps/api/geocode/json?address=" + cityName + "&sensor=false&key=" + API_key


	r = requests.get(link)
	myfile = r.json()

	latitude = myfile["results"][0]["geometry"]["location"]["lat"]
	longitude = myfile["results"][0]["geometry"]["location"]["lng"]

	results = [latitude, longitude]


	"""
	Returns an array. 
	results[0] is latitude and results[1] is longitude
	""" 
	return results


#getLatLong("Boston, MA")
