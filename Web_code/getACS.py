import os
import requests
import json

blockGroupList = []
blockGroupValues = []



acsVariablesMale = {"acs-widowed": "B12001_009E", "acs-divorced": "B12001_010E"}
acsVariablesFemale = {"acs-widowed": "B12001_018E", "acs-divorced": "B12001_019E"}
acsVariablesLanguage = {"acs-spanish-notAtAll":"B16004_030E", "acs-spanish-notWell":"B16004_029E", "acs-spanish-veryWell": "B16004_027E", "acs-asian-notAtAll":"B16004_040E", "acs-asian-notWell":"B16004_039E", "acs-asian-veryWell": "B16004_037E"}


def getACSdata(code, pop):
	state = code[0:2]
	county = code[2:5]
	tract = code[5:11]
	blockgroup = code [11:12]
	female = False
	male = False
	acsCodes = []
	popstring = []
	blockGroupList = []
	blockGroupValues = []
	interest = 0

	

	if "gender Male" in pop:
		male = True

	if "gender Female" in pop:
		female = True
		

	for p in pop:
		
		if "gender Female" in p or "gender Male" in p:
			continue 
		
		if "widowed" in p or "divorced" in p:
			if female:
				acsCodes.append(acsVariablesFemale[p])
				interest = interest + 1
			if male:
				acsCodes.append(acsVariablesMale[p])
				interest = interest + 1

		else:
			acsCodes.append(acsVariablesLanguage[p])
			interest = interest + 1

	if len(acsCodes) == 1:
		popstring = str(acsCodes[0])
	else:
		popstring = acsCodes[0]
		for element in range(1, len(acsCodes)):
			popstring = str(popstring) + "," + acsCodes[element]




	link = "http://api.census.gov/data/2010/acs5?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popstring) + "&for=block group:*&in=state:" + state + "+county:" + county + "+tract:" + tract
	r = requests.get(link)
	myfile = r.json()

	for blockGroup in range(1,len(myfile)):
		blockGroupList.append(myfile[blockGroup][-1])
		intblockGroupValues = []
		for demographic in range(0,interest):
			intblockGroupValues.append(myfile[blockGroup][demographic])
		blockGroupValues.append(intblockGroupValues)

	#print (blockGroupList, blockGroupValues)

	return (blockGroupList, blockGroupValues)


#getACS("080590120351000", ["B02001_001E", "B05009_023E"])