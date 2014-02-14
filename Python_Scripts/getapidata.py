import urllib
import os

pop = raw_input("Population code: ")
state = raw_input("State number: ")
county = raw_input("County number: ")
tract = raw_input("Tract number (or use * for all): ")

if tract == "*": 
	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + pop + ",NAME&for=tract:*&in=state:" + state + "+county:" + county
else:
	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + pop + ",NAME&for=block:*&in=state:" + state + "+county:" + county + "+tract:" + tract

f = urllib.urlopen(link)
myfile = f.read()
if "error" in myfile: 
	raise Exception("The API experienced an error with those codes")

script_path = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(script_path, "api_data.txt")

g = open(my_filename, "w")
g.write(myfile)
g.close()

print "The data is in api_data.txt"