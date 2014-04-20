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
	print link

	r = requests.get(link)
	text =  r.text
	print 'requests.status_code:', r.status_code
	print '<address> in text:', '<address>' in text

	places = [m.start() for m in re.finditer('<address>', text)]
	print places


	for place in places:
		print place
		address = find_between(text[int(place)::], "address", "</address>" )
		address = address.replace("<br>", " ");
		addressList.append(address)




	for address in addressList:
		print address
		lat = coor[0]
		lng = coor[1]
		currentLatLong = getLatLong.getLatLong(address)
		print currentLatLong
		if lat - mapDistance < float(currentLatLong[0]) < lat + mapDistance and lng - mapDistance < float(currentLatLong[1]) < lng + mapDistance:
			print "BUSINESS HERE!"
			businnesCoorList.append(currentLatLong)

	return businnesCoorList



#getAddresses((38.252665, -85.758456), "Louisville, KY", "coffee shop", 0.03)
#getAddresses([40.7358633, -73.9910835],"Union Square, NY","yoga studio",0.0152083333333)



