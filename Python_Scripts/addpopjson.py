import os
import requests
import json

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

r = requests.get(link)
myfile = r.json()

script_path = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(script_path, "api_data.json")
g = open(my_filename, "w")
g.write(json.dumps(myfile))
g.close()

poptotal = 0
for i in range(1, len(myfile)):
	pop_tract = int(myfile[i][0])
	poptotal = poptotal + pop_tract

print "The number of people in the population you specified is: " + str(poptotal)