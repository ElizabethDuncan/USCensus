
race = "Sex By Age (White Alone)"
gender = "Female"
agerange = 40
agerange_max = agerange+10

Concept_matches = []

#print codes["PCT012E071"]
printNextLabel = False
#iterate through the codes
for key in codes:
	#iterate through the concepts and labels in the codes
	for item in codes[key]:
		if item == "concept":
			if race in codes[key][item]:
				#Add keys that satisfy concept to dictionary
				Concept_matches.append(key)

for age in range(agerange, agerange_max):
	print age
	#Iterate through keys in concept dictionary
	for key in Concept_matches:
		#iterate through the concepts and labels in the codes
		for item in codes[key]:
			if item == "label":
				if gender + ": !! " + str(agerange) + " years" in codes[key][item] and "years" in codes[key][item]:
					
					print key

Concept_matches = []
				
				

		#print codes[key][item]