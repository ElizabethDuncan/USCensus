import gmerc
import getfips

def serve_tile( z, x, y):
    """
    /geom/<FeatureType>Tile/<z>/<x>/<y>.json
    """
    x1 = x * 256
    x2 = x1 + 255
    y1 = y * 256
    y2 = y1 + 255
    n, w = gmerc.px2ll(x1, y1, z)
    s, e = gmerc.px2ll(x2, y2, z)
    print n,w 
    print s,e
    
    s,w,n,e = [str(s), str(w), str(n), str(e)]
    bbox_wkt = "".join(["POLYGON((",
                        w+" "+s+",",
                        w+" "+n+",",
                        e+" "+n+",",
                        e+" "+s+",",
                        w+" "+s,
                        "))"])
    print bbox_wkt
   
    return n,w,s,e

lat1, lng1, lat2, lng2 = serve_tile(16, 17475, 24085)
print getfips.getfips(lat1,lng1)
print getfips.getfips(lat2,lng2)