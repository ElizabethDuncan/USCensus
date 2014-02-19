import os
import requests
import json

link = "http://api.census.gov/data/2010/sf1/variables.json"

r = requests.get(link)
myfile = r.json()

script_path = os.path.dirname(os.path.abspath(__file__))
my_filename = os.path.join(script_path, "api_var.json")
g = open(my_filename, "w")
g.write(json.dumps(myfile))
g.close()

print json.dumps(myfile, indent = 4, separators =(',', ':'))