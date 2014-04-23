import os
import requests
import json

blockGroupList = []
blockGroupValues = []



acsVariablesMale = {"acs-widowed": "B12001_009E", "acs-divorced": "B12001_010E"}
acsVariablesFemale = {"acs-widowed": "B12001_018E", "acs-divorced": "B12001_019E"}
acsVariablesLanguage = {"acs-spanish-notAtAll":"B16004_030E", "acs-spanish-notWell":"B16004_029E", "acs-spanish-veryWell": "B16004_027E", "acs-asian-notAtAll":"B16004_040E", "acs-asian-notWell":"B16004_039E", "acs-asian-veryWell": "B16004_037E"}
acsVariablesIncome = {"acs-less-10":"B19001_002E", "acs-10to15":"B19001_003E", "acs-15to20":"B19001_004E", "acs-20to25":"B19001_005E", "acs-25to30": "B19001_006E", "acs-30to35":"B19001_007E", "acs-35to40": "B19001_008E", "acs-40to45": "B19001_009E", "acs-45to50": "B19001_010E", "acs-50to60":"B19001_011E", "acs-60to75": "B19001_012E", "acs-75to100": "B19001_013E", "acs-100to125":"B19001_014E", "acs-125to150": "B19001_015E", "acs-150to200": "B19001_016E", "acs-200more": "B19001_017E"}

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

		elif "spanish" in p or "asian" in p:
			acsCodes.append(acsVariablesLanguage[p])
			interest = interest + 1
		else:
			acsCodes.append(acsVariablesIncome[p])
			interest = interest + 1

	if len(acsCodes) == 1:
		popstring = str(acsCodes[0])
	else:
		popstring = acsCodes[0]
		for element in range(1, len(acsCodes)):
			popstring = str(popstring) + "," + acsCodes[element]




	link = "http://api.census.gov/data/2010/acs5?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=" + str(popstring) + "&for=block group:*&in=state:" + state + "+county:" + county + "+tract:" + tract
	print link
	r = requests.get(link)
	myfile = r.json()

	for blockGroup in range(1,len(myfile)):
		blockGroupList.append(myfile[blockGroup][-1])
		intblockGroupValues = []
		for demographic in range(0,interest):
			intblockGroupValues.append(myfile[blockGroup][demographic])
		blockGroupValues.append(intblockGroupValues)

	print (blockGroupList, blockGroupValues)

	return (blockGroupList, blockGroupValues)

#getACSdata("36061005400", ['acs-widowed', 'acs-less-10','gender Female'])


