import os
import requests
import json

blockGroupList = []
blockGroupValues = []



acsVariablesMale = {"acs-widowed": "B12001_009E", "acs-divorced": "B12001_010E", "acs-nevermarried": "B12001_003E", "acs-married": "B12001_004E"}
acsVariablesFemale = {"acs-widowed": "B12001_018E", "acs-divorced": "B12001_019E", "acs-nevermarried": "B12001_012E", "acs-married": "B12001_013E"}
acsVariablesLanguage = {"acs-spanish-notAtAll":"B16004_030E", "acs-spanish-notWell":"B16004_029E", "acs-spanish-veryWell": "B16004_027E", "acs-asian-notAtAll":"B16004_040E", "acs-asian-notWell":"B16004_039E", "acs-asian-veryWell": "B16004_037E"}
acsVariablesIncome = {"acs-less-10":"B19001_002E", "acs-10to15":"B19001_003E", "acs-15to20":"B19001_004E", "acs-20to25":"B19001_005E", "acs-25to30": "B19001_006E", "acs-30to35":"B19001_007E", "acs-35to40": "B19001_008E", "acs-40to45": "B19001_009E", "acs-45to50": "B19001_010E", "acs-50to60":"B19001_011E", "acs-60to75": "B19001_012E", "acs-75to100": "B19001_013E", "acs-100to125":"B19001_014E", "acs-125to150": "B19001_015E", "acs-150to200": "B19001_016E", "acs-200more": "B19001_017E"}
acsVariablesEducation = {"acs-noschool": "B15002_003E,B15002_020E", "acs-12nodiplomaschool": "B15002_010E,B15002_027E","acs-hsgraduateschool": "B15002_011E,B15002_028E", "acs-somecollegeschool": "B15002_012E,B15002_013E,B15002_029E,B15002_030E", "acs-associatesschool": "B15002_014E,B15002_031E", "acs-bachelorschool": "B15002_015E,B15002_032E", "acs-mastersschool": "B15002_016E,B15002_033E", "acs-professionalschool": "B15002_017E,B15002_034E", "acs-doctorateschool": "B15002_018E,B15002_035E"}

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
	blockPopList = []
	interest = 0

	

	if "gender Male" in pop:
		male = True

	if "gender Female" in pop:
		female = True
		

	for p in pop:
		
		if "gender Female" in p or "gender Male" in p:
			continue 
		
		if "widowed" in p or "divorced" in p or "married" in p:
			if female:
				acsCodes.append(acsVariablesFemale[p])
				interest = interest + 1
			if male:
				acsCodes.append(acsVariablesMale[p])
				interest = interest + 1

		elif "spanish" in p or "asian" in p:
			acsCodes.append(acsVariablesLanguage[p])
			interest = interest + 1
		elif "school" in p:
			acsCodes.append(acsVariablesEducation[p])
			if "somecollege" in p:
				interest = interest + 4
				continue
			interest = interest + 2
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
	r = requests.get(link)
	myfile = r.json()

	link2 = "http://api.census.gov/data/2010/sf1?key=4be82289939444f20513cd7c3c3eafb42e0d9ccf&get=P0010001&for=block group:*&in=state:" + state + "+county:" + county + "+tract:" + tract
	r2 = requests.get(link2)
	myfile2 = r2.json()

	for blockGroup in range(1,len(myfile)):
		blockGroupList.append(myfile[blockGroup][-1])
		blockPopList.append(myfile2[blockGroup][0])
		intblockGroupValues = []
		for demographic in range(0,interest):
			intblockGroupValues.append(myfile[blockGroup][demographic])
		blockGroupValues.append(intblockGroupValues)


	return blockGroupList, blockGroupValues, blockPopList

#getACSdata("36061005400", ["acs-somecollegeschool", "acs-less-10","gender Female"])


