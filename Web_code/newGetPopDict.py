import os
import requests
import json

def getpop(poplist, code, level):
	""" Returns summed population info based on a list of population codes, a geographic FIPS code, and a 
	data level. 0 for counties in a state, 1 for tracts in a county, 2 for blocks in a tract """
	state = code[0:2]
	county = code[2:5]
	tract = code[5:11]

	popString = ""
	popString = poplist[0]

	if len(poplist) > 1:
		for pop in poplist[1::]:
			popString = str(popString) + "," + str(pop)
	

	popgroup = {}
	
	if level == 0: 
		link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popString) + ",NAME&for=county:*&in=state:" + state
	elif level == 1: 
		link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popString) + ",NAME&for=tract:*&in=state:" + state + "+county:" + county
	elif level == 2: 
		link = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popString) + ",NAME&for=block:*&in=state:" + state + "+county:" + county + "+tract:" + tract
	else:
		raise Exception("Data level not valid")
	print link
	r = requests.get(link)
	myfile = r.json()

	"""
	script_path = os.path.dirname(os.path.abspath(__file__))
	my_filename = os.path.join(script_path, "api_data" + str(i) + ".json")
	g = open(my_filename, "w")
	g.write(json.dumps(myfile))
	g.close() """

	def sumgroups(pop_unit, name):
		if name in popgroup: 
			popgroup[name] += pop_unit
		else:
			popgroup[name] = pop_unit

	for j in range(1, len(myfile)):
		num = len(poplist)
		for k in range(0, num):
			pop_unit = int(myfile[j][k])
			if level == 0: 
				name = str(myfile[j][2 + num])
			if level == 1: 
				name = str(myfile[j][3 + num])
			if level == 2: 
				name = str(myfile[j][num + 4])
			sumgroups(pop_unit, name)

	return popgroup


#data = getpop(["P0030002", "P0030003", "P0030004","P0030005","P0030006","P0030007","P0030008"], "44009051306", 1)
#print data
