
def getCodes(myrace, mygender, myage):
	race = myrace
	gender = mygender
	agerange = int(myage)
	if agerange != 0:
		agerange_max = agerange+10
	else:
		agerange = agerange + 1
		agerange_max = agerange+19

	Concept_matches = []
	Key_matches = []

	#print codes["PCT012E071"]
	printNextLabel = False
	#iterate through the codes
	for key in codes:
		#iterate through the concepts and labels in the codes
		if race in codes[key].get("concept", []):
			Concept_matches.append(key)

	for age in range(agerange, agerange_max):
		#Iterate through keys in concept dictionary
		for key in Concept_matches:
			if gender + ": !! " + str(age) + " year" in codes[key]["label"]:
				Key_matches.append(key)
				#there are occasional instances where more than one key matches the race, gender and age
				#we break so as only to count each age group once.
				break


	Concept_matches = []


	return Key_matches


"""
race = "Sex By Age (White Alone)"
gender = "Female"
agerange = 20
getCodes(race, gender, agerange)
"""
