"""
This script contains takes the string location and string description of business
and scrapes yelp for similar businesses
Returns a maximum of 10 businesses in one location
"""

import requests
import json
import re
import getLatLong

def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return False

def getAddresses(coor, location, descrip, mapDistance):
	addressList = []
	businnesCoorList = []
	link = "http://www.yelp.com/search?find_desc=" + str(descrip) + "&find_loc=" + str(location) + "&ns=1&ls=ba0120fc3b21754c"


	r = requests.get(link)
	text =  r.text

	places = [m.start() for m in re.finditer('<address>', text)]


	for place in places:
		address = find_between(text[int(place)::], "address", "</address>" )
		address = address.replace("<br>", " ");
		addressList.append(address)




	for address in addressList:
		lat = coor[0]
		lng = coor[1]
		currentLatLong = getLatLong.getLatLong(address)
		print currentLatLong
		if lat - mapDistance < float(currentLatLong[0]) < lat + mapDistance and lng - mapDistance < float(currentLatLong[1]) < lng + mapDistance:
			print "BUSINESS HERE!"
			businnesCoorList.append(currentLatLong)

	return businnesCoorList


#getAddresses((38.252665, -85.758456), "Louisville, KY", "coffee shop", 0.03)