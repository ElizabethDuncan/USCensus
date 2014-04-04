import sys
import requests
import os
import multiprocessing
import gmerc2


def getAlbertStuff():
	print "Starting"

	zoom = 16
	empty = []
	lat = 18
	latMax = 72
	lngInitial = -180
	lngMax = -66

	increment = 1

	f = open('range.txt','w')

	while lat < latMax:
		lng = lngInitial
		lat = lat + increment

		while lng < lngMax:

			x1, y1 = gmerc2.ll2px(lat, lng, zoom)
			x = x1 / 256 
			y = y1 / 256

			#write to 
			current = "lat and lng: " + str(lat) + " " + str(lng) + "\n"
			f.write(current)
			current = "x and y: " + str(x) + " " + str(y) + "\n"
			f.write(current) # python will convert \n to os.linesep
			lng = lng + increment
	
	f.close()

			
			

	
			

			



getAlbertStuff()