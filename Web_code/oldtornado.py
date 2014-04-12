# Access this webpage from a browser at url: http://127.0.0.1:8888/

from flask import *
import json
#TODO: MOVE CODES_DATA.PY INTO THIS FILE!
import codes_data
import getpopdict
import getLatLong
import getfips
import coordinates
import fromFIPSlisttoLatLong
import censusTracts
import getACS


app = Flask(__name__)
app.debug = True
app.vars = {}
app.city = []
app.cityID = ""
app.races = []
app.genders = []
app.ages = []
app.keys = []
app.acsCodes = []

#A dictionary keyed to Fips that contains a duple of LatLong and then the value for the requested demographic
FipsLatLongAndValue = {}
listofFips = []
listofFipsINTS = []
listofCoords = []
listofValues = []
listOfLatLng = []
listofAcsValues = []
listofShades = []
listofAcsValueShades = []
listofValueShades = []

codeLookup = {'race AfricanAmerican': 'Sex By Age (Black Or African American Alone)', 'race white': 'Sex By Age (White Alone)', 'race Latino': 'Sex By Age (Hispanic Or Latino)', 'race Asian': 'Sex By Age (Asian Alone)', 'race Hawaiian': '(Native Hawaiian And Other Pacific Islander Alone)', 'race NativeAmerican': 'Sex By Age (American Indian And Alaska Native Alone)', 'race Multiracial': 'Sex By Age (Two Or More Races)', 'gender Male': 'Male', 'gender Female': 'Female', 'age 0': '0', 'age 20': '20', 'age 30': '30', 'age 40': '40', 'age 50': '50', 'age 60': '60', 'age 70': '70', 'age 80': '80'}

@app.route("/")
def index():
	return render_template("index.html")

@app.route("/The_Data")
def The_Data():
	return render_template("The_Data.html")

@app.route("/The_Process")
def The_Process():
	return render_template("The_Process.html")

@app.route("/About_Us")
def About_Us():
	return render_template("About_Us.html")

@app.route('/getsurveyresults', methods=['POST'])
def processData():
	#Get race data
	app.vars['race AfricanAmerican'] = request.form.get('race AfricanAmerican')
	app.vars['race white'] = request.form.get('race White')
	app.vars['race Latino'] = request.form.get('race Latino')
	app.vars['race Asian'] = request.form.get('race Asian')
	app.vars['race Hawaiian'] = request.form.get('race Hawaiian')
	app.vars['race NativeAmerican'] = request.form.get('race NativeAmerican')
	app.vars['race Multiracial'] = request.form.get('race Multiracial')

	#get age data
	app.vars['gender Male'] = request.form.get('gender Male')
	app.vars['gender Female'] = request.form.get('gender Female')

	#Get age data
	app.vars['age 0'] = request.form.get('age 0')
	app.vars['age 20'] = request.form.get('age 20')
	app.vars['age 30'] = request.form.get('age 30')
	app.vars['age 40'] = request.form.get('age 40')
	app.vars['age 50'] = request.form.get('age 50')
	app.vars['age 60'] = request.form.get('age 60')
	app.vars['age 70'] = request.form.get('age 70')
	app.vars['age 80'] = request.form.get('age 80')

	app.vars['acs-widowed'] = request.form.get('widowed')
	app.vars['acs-divorced'] = request.form.get('divorced')
	app.vars['acs-spanish-notAtAll'] = request.form.get('spanish-notAtAll')
	app.vars['acs-spanish-notWell'] = request.form.get('spanish-notWell')
	app.vars['acs-spanish-veryWell'] = request.form.get('spanish-veryWell')
	app.vars['acs-asian-notAtAll'] = request.form.get('asian-notAtAll')
	app.vars['acs-asian-notWell'] = request.form.get('asian-notWell')
	app.vars['acs-asian-veryWell'] = request.form.get('asian-veryWell')
	
	#From name of city requested, get Latitude and Longitude
	latAndLong = getLatLong.getLatLong(str(request.form.get('city')))
	lat = latAndLong[0]
	lng = latAndLong[1]

	#Get list of tracts from that latitude, longitude

	#Note - cast as a string!
	app.cityID = str(getfips.getfips(lat, lng))


	#add each demographic to the corresponding variable list (race, gender and age)
	for demographic in app.vars:
		if app.vars[demographic] == 'True':
			data = True
			if "race" in demographic:
				app.races.append(demographic)
			if "gender" in demographic:
				app.genders.append(demographic)
			if "age" in demographic:
				app.ages.append(demographic)
			if "acs" in demographic or "gender" in demographic:
				#Gets acs checked data as well as requested gender
				app.acsCodes.append(demographic)


	#Print list of demographics for debugging (City should be listed first
	for race in app.races:
		for gender in app.genders:
			for age in app.ages:
				app.keys.append(codes_data.getCodes(codeLookup[race], codeLookup[gender], codeLookup[age]))
	
	newKeys = [val for subl in app.keys for val in subl]

	allTracts = censusTracts.listTracts(app.cityID)
	#tract = app.cityID
	#For all the tracts in the specified city (county area), sum the number of people in the specified codes
	#Last paramter is 1, so that we get tract data (in the county)
	listofCoords = []

	allTractsLatLng = fromFIPSlisttoLatLong.getLatLngFromFIPS(allTracts)
	iterator = 0
	length = len(allTracts)
	mapDistance = 1.5 / length

	for tract in allTracts:
		#Get lat long of tract
		z = 16

		if tract is app.cityID or (lat - mapDistance < float(allTractsLatLng[iterator][0]) < lat + mapDistance and lng - mapDistance < float(allTractsLatLng[iterator][1]) < lng + mapDistance):

			#Get ACS data
			ACSdata = getACS.getACSdata(tract, app.acsCodes)

			listofCoords = []
			data = getpopdict.getpop(newKeys, tract, 2)

			#JUST ADDED
			
			#For every block in the current tract, get lat and long
			for item in data:
				blockFIPS = tract[0:11] +  item



				if blockFIPS not in listofFips:
					blockGroupIndex = blockFIPS[11:12]
					listofFips.append(blockFIPS)
					listofFipsINTS.append(int(blockFIPS))

					acsSum = 0
					for element in ACSdata[1][int(blockGroupIndex)-1]:
						acsSum = acsSum + int(element)

					listofAcsValues.append(acsSum)

					listofValues.append(data[item])
				
			
			#Get coordinates from FIPS codes
			listOfLatLng = fromFIPSlisttoLatLong.getLatLngFromFIPS(listofFips)
			for latAndLong in listOfLatLng:
				intermediate =  coordinates.getblockcoor(float(latAndLong[0]),float(latAndLong[1]),z)
				listofCoords.append(intermediate[1])


			#Clear app.vars so subsequent queries can occur
			app.vars = {}

			#Load html
			
		
		iterator = iterator + 1

	#print listofCoords
	lst = coordinates.getblockcoor(lat,lng,z)
	geoid = lst[0]
	coor = lst[1]

	#Iterate through listofValues and listofAcsValues to convert them to a shadeValue
	acsMax = max(listofAcsValues)
	acsMax = float(acsMax)
	valueMax = max(listofValues)
	valueMax = float(valueMax)

	for acsValue in listofAcsValues:
		if float(acsValue/float(acsMax)) < 0.1:
			current = 0.1
		else: 
			current = acsValue/acsMax
		listofAcsValueShades.append(current)

	for value in listofValues:
		if value/float(valueMax) < 0.1:
			current = 0.1
		else: 
			current = value/valueMax
		listofValueShades.append(current)

	for item in range(0, len(listofValueShades)):
		shade = listofValueShades[item] + listofAcsValueShades[item]
		shade = shade /2

		listofShades.append(shade)

	print listofValues
	print listofFips
	print listofShades
	
	return render_template("getsurveyresults.html", data1 = listofFipsINTS, data = listofCoords, data2 = listofValues, dataShades = listofShades, lat = lat, lng = lng, z = z, coor = coor)


"""
@app.route("/team")
def team():
	json_team_data = open("data/team.json")
	team_data = json.load(json_team_data)
	json_team_data.close()
	return render_template("team.html", team=team_data)
	"""

if __name__ == "__main__":
	app.run()