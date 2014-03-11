## Douglas Blank
## Fall 2011
#
# Documentation on low-level projection functions:
# http://code.google.com/apis/maps/documentation/reference.html#GMercatorProjection
#
# Based on:
# http://code.google.com/p/gheat/source/browse/trunk/__/lib/python/gmerc.py

#from Graphics import *
#import Myro
import math

"""
There are three global variables that control the display of the map:
  width, height, and zoom. Zoom is one of 31 values, from 0 to 30.
  Height and width are in pixels.
"""

# Cache for saving state colors:
state_colors = {}

def ll2xy(lat, lng):
    """
    Give a latitude and longitude, return a x,y in terms of this map window.
    """
    retval = ll2px(lat, lng, zoom)
    return (retval[0] - center[0] + width/2,
            retval[1] - center[1] + height/2)

def xy2ll(x, y):
    """
    Given a x,y in this map window, return the global latitude, longitude
    """
    retval = px2ll(x - width/2 + center[0],
                   y - height/2 + center[1], zoom)
    return retval[0], 360 - retval[1]

def ll2px(lat, lng, zoom):
    """
    Given a latitude, longitud, return a global x,y.
    """
    cbk = CBK[zoom]
    x = int(round(cbk + (-lng * CEK[zoom])))
    foo = math.sin(lat * math.pi / 180)
    if foo < -0.9999:
        foo = -0.9999
    elif foo > 0.9999:
        foo = 0.9999
    y = int(round(cbk + (0.5 * math.log((1+foo)/(1-foo)) * (-CFK[zoom]))))
    return (x, y)

def px2ll(x, y, zoom):
    """
    Given a global x, y, return a latitude, longitude.
    """
    foo = CBK[zoom]
    lng = (x + foo) / CEK[zoom]
    bar = (y - foo) / -CFK[zoom]
    blam = 2 * math.atan(math.exp(bar)) - math.pi / 2
    lat = blam / (math.pi / 180)
    return (lat, lng)

def drawStates(win, color=None):
    """
    Draw all states in a given color, or random.
    """
    retval = {}
    for state in states:
        retval[state] = drawState(win, state, color)
    return retval

def drawState(win, state, color=None):
    retval = []
    for list in states[state]:
        polygon = Polygon(*[ll2xy(pair[0], pair[1]) for pair in list])
        if color is not None:
            state_colors[state] = Color(color)
        elif state not in state_colors:
            state_colors[state] = Color(Myro.pickOne(Myro.getColorNames()))
        polygon.fill = state_colors[state]
        polygon.draw(win)
        retval.append(polygon)
    return retval

def readStates(filename):
    retval = {}
    fp = open(filename)
    for line in fp:
        abbrev_index, data = line.strip().split(";", 1)
        abbrev, index = abbrev_index[0:2], abbrev_index[2:]
        polys = retval.get(abbrev, [])
        state = []
        for pair in data.split(";"):
            longitude, latitude = pair.split(",")
            state.append((float(longitude), float(latitude)))
        polys.append(state)
        retval[abbrev] = polys
    return retval

def readCapitals(filename):
    retval = {}
    fp = open(filename)
    for line in fp:
        if line.startswith("#"):
            continue
        abbrev, data = line.strip().split(",", 1)
        state, capital, lat, lng = data.split(",") # Idaho,Boise,43.613739,116.237651
        retval[abbrev] = {"name": state, "capital": capital, "longitude": float(lat),
                          "latitude": float(lng)}
    return retval

def drawCapitals(win):
    for capital in capitals:
        x, y = ll2xy(capitals[capital]["longitude"],
                     capitals[capital]["latitude"])
        p = Point(x, y + 10)
        text = Text(p, capitals[capital]["capital"])
        text.fontSize = 8
        text.color = Color("white")
        text.draw(win)
        p = Point(x-1, y + 10 - 1)
        text = Text(p, capitals[capital]["capital"])
        text.fontSize = 8
        text.color = Color("black")
        text.draw(win)
        #p = Point(x, y)
        d = Rectangle((x, y), (x+1, y+1))
        #d.fill = Color("white")
        d.draw(win)

def getLLClick():
    x, y = getMouseNow()
    return xy2ll(x, y)

def displayControls(win):
    zoomin = Rectangle((width - 50, 0), (width, height))
    zoomin.fill = Color("white")
    zoomin.draw(win)
    zin = Text((width - 25, height/2), "Zoom In")
    zin.rotate(-90)
    zin.draw(win)
    zoomout = Rectangle((0, 0), (50, height))
    zoomout.fill = Color("white")
    zoomout.draw(win)
    zout = Text((25, height/2), "Zoom Out")
    zout.rotate(90)
    zout.draw(win)

# Constants:

CBK = [128, 256, 512, 1024, 2048, 4096, 8192, 16384, 32768, 65536, 131072, 262144, 524288, 1048576, 2097152, 4194304, 8388608, 16777216, 33554432, 67108864, 134217728, 268435456, 536870912, 1073741824, 2147483648, 4294967296, 8589934592, 17179869184, 34359738368, 68719476736, 137438953472]
CEK = [0.7111111111111111, 1.4222222222222223, 2.8444444444444446, 5.688888888888889, 11.377777777777778, 22.755555555555556, 45.51111111111111, 91.02222222222223, 182.04444444444445, 364.0888888888889, 728.1777777777778, 1456.3555555555556, 2912.711111111111, 5825.422222222222, 11650.844444444445, 23301.68888888889, 46603.37777777778, 93206.75555555556, 186413.51111111112, 372827.02222222224, 745654.0444444445, 1491308.088888889, 2982616.177777778, 5965232.355555556, 11930464.711111112, 23860929.422222223, 47721858.844444446, 95443717.68888889, 190887435.37777779, 381774870.75555557, 763549741.5111111]
CFK = [40.74366543152521, 81.48733086305042, 162.97466172610083, 325.94932345220167, 651.8986469044033, 1303.7972938088067, 2607.5945876176133, 5215.189175235227, 10430.378350470453, 20860.756700940907, 41721.51340188181, 83443.02680376363, 166886.05360752725, 333772.1072150545, 667544.214430109, 1335088.428860218, 2670176.857720436, 5340353.715440872, 10680707.430881744, 21361414.86176349, 42722829.72352698, 85445659.44705395, 170891318.8941079, 341782637.7882158, 683565275.5764316, 1367130551.1528633, 2734261102.3057265, 5468522204.611453, 10937044409.222906, 21874088818.445812, 43748177636.891624]

width, height, zoom = 700, 400, 4
center_ll = (38.572954, 95.189283) # center of map
center = ll2px(center_ll[0], center_ll[1], zoom) # center of map, in global XY

states = readStates("states.dat")
capitals = readCapitals("capitals.dat")

def demo():
    global width, height, zoom, center_ll, center
    win = Window("Calico GIS", width, height)
    drawStates(win)
    drawCapitals(win)
    displayControls(win)
    while win.isRealized():
        x, y = getMouse()
        if x < 50:
            zoom = max(0, zoom - 1)
        elif x > width - 50:
            zoom = min(30, zoom + 1)
        else:
            center_ll = xy2ll(x, y)
        print("Center at (%s North, %s West) at zoom %s" % (center_ll[0], center_ll[1], zoom))
        center = ll2px(center_ll[0], center_ll[1], zoom) # center of map, in global XY
        win.clear()
        drawStates(win)
        drawCapitals(win)
        displayControls(win)

if __name__ == "<module>":
    demo()