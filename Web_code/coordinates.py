import gmerc2
import getfips
import requests
import json

def getblockcoor(lat,lng, zoom):
    """ Input lat, lng, zoom level, return block FIPS code, map coordinates """

    x1, y1 = gmerc2.ll2px(lat, lng, zoom)
    x = x1 / 256 
    y = y1 / 256

    geoid = getfips.getfips(lat,lng)

    link = "http://censusmapmaker.com/geom/CensusBlockTile/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".json"
    r = requests.get(link)
    myfile = r.json()

    for i in range(0, len(myfile['features'])):
        mydict = myfile['features'][i] 
        if mydict['id'] == geoid:
            coor = mydict['geometry']['coordinates'][0][0]
   
    return  geoid, coor

#coor1 = (42.9845581343, -84.0069580078)
#getblockcoor(coor1[0], coor1[1], 16)