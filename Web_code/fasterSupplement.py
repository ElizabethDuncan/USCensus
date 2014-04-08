import sys
import requests
import os
import multiprocessing
import gmerc2


def getAlbertStuff():
	print "Starting"

	# zoom = 16
	# empty = []
	# lat = 18
	# latMax = 72
	# lngInitial = -180
	# lngMax = -66

	zoom = 16
	empty = []
	lat = 24.5
	latMax = 49
	lngInitial = -124.73
	lngMax = -66.962
	lngNew = -67
	latNew = 30


	smallincrement = 0.3
	bigIncrement = 0.001

	while lat < latMax:
		lng = lngInitial
		lat = lat + bigIncrement

		while lng < lngMax:

			x1, y1 = gmerc2.ll2px(lat, lng, zoom)
			x = x1 / 256 
			y = y1 / 256
			
			name = str('./CensusBlockTile/' + str(zoom) + '-'+ str(x) + '-' + str(y))
			fileName = name +".json"

			value = os.path.isfile(fileName)

			if value:
				print "file exists " + str(x) + " " + str(y)
				lng = lng + bigIncrement
				continue

			link = "http://censusmapmaker.com/geom/CensusBlockTile/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".json"
			try:

				r = requests.get(link)
				data = r.json()

				if data == empty:
					print "empty" + str(x) + " " + str(y)
					lng = lng + smallincrement
					pass
				else:
					print link
					file = open(fileName,'w')   # Trying to create a new file or open one
					file.write(str(data))
					file.close()
					lng = lng - 0.5
					lng = lng + bigIncrement

			except:
				print "Null page"
				data = []
				lng = lng + smallincrement
			

			
			

	
			

			



getAlbertStuff()