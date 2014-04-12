"""
This script contains getLatLngFromFIPS, which takes in a blockID FIPS code and returns a LatLong
Uses TigerWeb geo data
THIS SLOWS THE WEBSITE SIGNIFICANTLY
"""

import requests
import json
import gmerc2

states= {
	"01": "al", 
	"02": "ak", 
	"04": "az", 
	"05":"ar", 
	"06":"ca", 
	"08": "co", 
	"09": "ct", 
	"10":"de", 
	"11":"dc", 
	"12": "fl", 
	"13": "ga", 
	"15":"hi", 
	"16":"id", 
	"17":"il", 
	"18":"in", 
	"19":"ia", 
	"20":"ks", 
	"21":"ky", 
	"22":"la", 
	"23":"me", 
	"24":"md", 
	"25":"ma", 
	"26":"mi",
	"27":"mn",
	"28":"ms", 
	"29":"mo", 
	"30":"mt", 
	"31":"ne", 
	"32":"nv", 
	"33":"nh", 
	"34":"nj", 
	"35":"nm", 
	"36":"ny", 
	"37":"nc", 
	"38":"nd", 
	"39":"oh", 
	"40":"ok", 
	"41":"or", 
	"42":"pa", 
	"44":"ri", 
	"45":"sc", 
	"46":"sd", 
	"47":"tn", 
	"48":"tx",
	"49":"ut", 
	"50":"vt", 
	"51":"va", 
	"53":"wa", 
	"54":"wv", 
	"55": "wi", 
	"56":"wy" }

latLngList = []
def find_between( s, first, last ):
    try:
        start = s.index( first ) + len( first )
        end = s.index( last, start )
        return s[start:end]
    except ValueError:
        return ""



def getLatLngFromFIPS(fipsList, zoom):
	FipsPixelDict = {}

	#Make only one web connection
	initialfips = fipsList[0]
	state = initialfips[0:2]
	county = initialfips[2:5]
	tract = initialfips[5:11]
	block = initialfips[11:15]

	print states[state]
	print county

	link = "http://tigerweb.geo.census.gov/tigerwebmain/Files/tigerweb_tab10_tabblock_2010_" + states[state] + "_" + county + ".html"
	r = requests.get(link)
	text =  r.text

	for fips in fipsList:
		state = fips[0:2]
		county = fips[2:5]
		tract = fips[5:11]
		block = fips[11:15]

		latLongAndStuff = find_between(text, fips, "</tr>")
		
		latitude = find_between(latLongAndStuff, "<td headers=\"header20\">", "</td>")
		if "+" in latitude:
			latitude = latitude.split("+")
			latLength = len(latitude)
			latitude = latitude[latLength-1]
		longitude = find_between(latLongAndStuff, "<td headers=\"header21\">", "</td>")
		if "+" in longitude:
			longitude = longitude.split("+")
			longLength = len(longitude)
			longitude = longitude[longLength-1]

		pixels = getpixels(latitude, longitude, zoom)
		if FipsPixelDict.has_key(pixels) == False: 
			FipsPixelDict[pixels] = [fips]
		if FipsPixelDict.has_key(pixels) == True:
			FipsPixelDict[pixels] += [fips]

	return FipsPixelDict

def getpixels(lat, lng, zoom):
	x1, y1 = gmerc2.ll2px(float(lat), float(lng), zoom)
	x = x1 / 256 
	y = y1 / 256

	pixels = (int(x), int(y))
	return pixels 

		


#getLatLngFromFIPS("080370001001001", 16)



