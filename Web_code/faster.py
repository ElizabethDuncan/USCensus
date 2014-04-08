import sys
import requests
import os
import multiprocessing
import gmerc2


def getAlbertStuff():
	print "Creating text files"

	zoom = 16
	empty = []

	for lat in range(18, 72):
		for lng in range(-180, -66):

			x1, y1 = gmerc2.ll2px(lat, lng, zoom)
			x = x1 / 256 
			y = y1 / 256
			
			name = str('./CensusBlockTile/' + str(zoom) + '-'+ str(x) + '-' + str(y))
			fileName = name +".json"

			value = os.path.isfile(fileName)

			if value:
				print "file exists " + str(x) + " " + str(y)
				continue

			link = "http://censusmapmaker.com/geom/CensusBlockTile/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".json"
			try:

				r = requests.get(link)
				data = r.json()

				if data == empty:
					print "empty" + str(x) + " " + str(y)
					pass
				else:
					print link
					file = open(fileName,'w')   # Trying to create a new file or open one
					file.write(str(data))
					file.close()

			except:
				print "Null page"
				data = []
	
			

			



getAlbertStuff()