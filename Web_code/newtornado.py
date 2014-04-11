# Access this webpage from a browser at url: http://127.0.0.1:8888/

from flask import *
import json
#TODO: MOVE CODES_DATA.PY INTO THIS FILE!
import codes_data
import getpopdict
import getLatLong
import getfips
import fromFIPSlisttoLatLong
import censusTracts
import getACS
import fromFIPStoPixels
import pixelcoordinates


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
listofFipsCoordsDicts = []
listofFipsINTS = []
listofFips = []
listofValues = []
listOfLatLng = []
listofAcsValues = []
listofShades = []
listofAcsValueShades = []
listofValueShades = []
FipsPixelDict = {}
FipsCoordsDict = {}

codeLookup = {'race AfricanAmerican': 'Sex By Age (Black Or African American Alone)', 'race White': 'Sex By Age (White Alone)', 'race Latino': 'Sex By Age (Hispanic Or Latino)', 'race Asian': 'Sex By Age (Asian Alone)', 'race Hawaiian': '(Native Hawaiian And Other Pacific Islander Alone)', 'race NativeAmerican': 'Sex By Age (American Indian And Alaska Native Alone)', 'race Multiracial': 'Sex By Age (Two Or More Races)', 'gender Male': 'Male', 'gender Female': 'Female', 'age 0': '0', 'age 20': '20', 'age 30': '30', 'age 40': '40', 'age 50': '50', 'age 60': '60', 'age 70': '70', 'age 80': '80'}

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
	data = ['race AfricanAmerican','race White', 'race Latino', 'race Asian', 'race Hawaiian', 'race NativeAmerican','race Multiracial', 'gender Male', 'gender Female', 'age 0', 'age 20', 'age 30', 'age 40', 'age 50','age 60','age 70','age 80']
	data_acs = ['widowed','divorced', 'spanish-notAtAll', 'spanish-notWell','spanish-veryWell', 'asian-notAtAll','asian-notWell', 'asian-veryWell']

	for i in range(0, len(data)): 
		app.vars[data[i]] = request.form.get(data[i])
	for i in range(0, len(data_acs)): 
		app.vars['acs-' + data_acs[i]] = request.form.get(data_acs[i])

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

			#Clear app.vars so subsequent queries can occur
			app.vars = {}
			
			#Get coordinates from FIPS codes

			d2 = fromFIPStoPixels.getLatLngFromFIPS(listofFips, z)
			for k, v in d2.iteritems():
				if FipsPixelDict.has_key(k) == False: 
					FipsPixelDict[k] = v
				elif FipsPixelDict.has_key(k) == True:
					FipsPixelDict[k] += v
			#Load html
				
		iterator = iterator + 1

			#print FipsPixelDict
	for k,v in FipsPixelDict.iteritems():
		intermediate =  pixelcoordinates.getblockcoor(v, k[0], k[1], z)
		if len(intermediate.keys()) > 1:
			for k2, v2 in intermediate.iteritems():
				FipsCoordsDict[k2] = v2
		else:
			k2 = intermediate.keys()[0]
			v2 = intermediate.values()[0]
			FipsCoordsDict[k2] = v2

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
	
	return render_template("fixing.html", data = FipsCoordsDict, data2 = listofValues, dataShades = listofShades, lat = lat, lng = lng, z = z)


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