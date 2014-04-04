import os
import requests
import json

listofTracts = []

def listTracts(code):
	state = code[0:2]
	county = code[2:5]
	tract = code[5:11]
	block = code[11:15]

	pop = "P0010001"

	link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + pop + ",NAME&for=tract:*&in=state:" + state + "+county:" + county

	r = requests.get(link)
	myfile = r.json()

	for item in myfile:
		tractID = item[4]
		if tractID == "tract":
			pass
		else:
			listofTracts.append(str(state+county+tractID))

	return listofTracts


#listTracts("080050056221001")