import gmerc2
import getfips
import requests
import simplejson as json
import os

def getblockcoor(lat,lng, zoom):
    """ Input lat, lng, zoom level, return block FIPS code, map coordinates """
    #print str(lat) + " " + str(lng)
    x1, y1 = gmerc2.ll2px(lat, lng, zoom)
    x = x1 / 256 
    y = y1 / 256

    geoid = getfips.getfips(lat,lng)

    name = str('./CensusBlockTile/' + str(zoom) + '-'+ str(x) + '-' + str(y))
    fileName = name +".json"

    #value = os.path.isfile(fileName)
    value = False

    if value:

        #TODO: FIX SO THIS WORKS!!!
        print "file exists!"
        json_data=open(fileName)
        json_data_text = json_data.read()
        print "BEFORE"
        print json_data_text
        json_data_text.decode("utf-8").replace(u"\u2022", "\"")
        json_data_text.replace(u"'", "\"")
        print "AFTER"
        print json_data_text
        read = json.loads(json_data_text)
        for elem in read:
            print elem["type"]
        n = json.dumps(json_data_text)  
        myfile = json.loads(n)
        
        print myfile['type']
        print type(myfile)
        json_data.close()
    else:
        link = "http://censusmapmaker.com/geom/CensusBlockTile/" + str(zoom) + "/" + str(x) + "/" + str(y) + ".json"
        #print link
        r = requests.get(link)
        myfile = r.json()


    for i in range(0, len(myfile['features'])):
        mydict = myfile['features'][i] 
        if mydict['id'] == geoid:
            coor = mydict['geometry']['coordinates'][0][0]
   
    return  geoid, coor

#coor1 = (42.9845581343, -84.0069580078)
#print getblockcoor(coor1[0], coor1[1], 16)