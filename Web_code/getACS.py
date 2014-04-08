import os
import requests
import json

blockGroupList = []
blockGroupValues = []


def getACS(code, pop):
	state = code[0:2]
	county = code[2:5]
	tract = code[5:11]
	blockgroup = code [11:12]

	popstring = pop[0]
	print popstring


	if len(pop) > 1:
		pop = pop[1:]
		for element in pop:
			popstring = popstring + "," + element


	print popstring
	link = "http://api.census.gov/data/2010/acs5?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popstring) + "&for=block group:*&in=state:" + state + "+county:" + county + "+tract:" + tract
	print link
	r = requests.get(link)
	myfile = r.json()

	for blockGroup in range(1,len(myfile)):
		blockGroupList.append(myfile[blockGroup][6])
		print len(pop)
		intblockGroupValues = []
		for demographic in range(0,len(pop)+1):
			intblockGroupValues.append(myfile[blockGroup][demographic])
		blockGroupValues.append(intblockGroupValues)


	return (blockGroupList, blockGroupValues)


getACS("080590120351000", ["B02001_001E", "B05009_023E"])