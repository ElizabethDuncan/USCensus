import urllib
import os
import string 

pop = raw_input("Population code: ")
state = raw_input("State number: ")
county = raw_input("County number (or use * for all): ")
if county != "*":
	tract = raw_input("Tract number (or use * for all): ")

if county == "*": 
	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=P0010001,NAME&for=county:*&in=state:" + state
elif tract == "*": 
	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + pop + ",NAME&for=tract:*&in=state:" + state + "+county:" + county
else:
	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + pop + ",NAME&for=block:*&in=state:" + state + "+county:" + county + "+tract:" + tract

f = urllib.urlopen(link)
myfile = f.read()
if "error" in myfile or len(myfile) == 0: 
	raise Exception("The API experienced an error with those codes")

script_path = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(script_path, "api_data.txt")

g = open(my_filename, "w")
g.write(myfile)
g.close()

poptotal = 0
with open(my_filename) as h:
        for i, l in enumerate(h):
        	if i > 0: 
        		line = l.strip('\n').strip(']').strip('[').strip('],').split(',')
        		pop_tract = line[0].strip('"')
        		poptotal = poptotal + int(pop_tract)

print "The number of people in the population you specified is: " + str(poptotal)