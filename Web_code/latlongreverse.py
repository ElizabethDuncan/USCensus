import gmerc2
import getfips
import requests
import json

coor1 = (42.9845581343, -84.0948486328)
coor2 = (42.9805552456, -84.0893769264)

def getblockcoor(lat,lng, zoom):
    """ Input lat, lng, return block FIPS code and map coordinates """

    x1, y1 = gmerc2.ll2px(lat, lng, zoom)
    x = x1 / 256 
    y = y1 / 256
    link = "http://censusmapmaker.com/geom/CensusBlockTile/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".json"
    r = requests.get(link)
    myfile = r.json()
    mydict = myfile['features'][0]
    coor = mydict['geometry']['coordinates'][0][0]
    geoid = mydict['id']
    print geoid 
    print coor
    return  geoid, coor

getblockcoor(coor1[0], coor1[1], 16)