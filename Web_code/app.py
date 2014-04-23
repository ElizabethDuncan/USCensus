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
import newGetPopDict
import scrapeYelp
import pickle

app = Flask(__name__)

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
	app.races = []
	app.genders = []
	app.ages = []
	app.acsCodes = []
	allTractsLatLng = []

	app.debug = True
	app.vars = {}
	app.city = []
	app.cityID = ""
	app.races = []
	app.genders = []
	app.ages = []
	app.keys = []
	app.acsCodes = []
	tractAndPop = {}
	blockAndPop = {}

	#A dictionary keyed to Fips that contains a duple of LatLong and then the value for the requested demographic
	listofFips = []
	listofValues = []
	listofAcsValues = []
	listofShades = []
	listofAcsValueShades = []
	listofValueShades = []
	FipsPixelDict = {}
	MegaDict = {}
	ValueDict = {}
	AcsDict = {}

	displayingSomething = False


	
	#Get race data
	data = ['race AfricanAmerican','race White', 'race Latino', 'race Asian', 'race Hawaiian', 'race NativeAmerican','race Multiracial', 'gender Male', 'gender Female', 'age 0', 'age 20', 'age 30', 'age 40', 'age 50','age 60','age 70','age 80']
	data_acs = ['widowed','divorced', 'spanish-notAtAll', 'spanish-notWell','spanish-veryWell', 'asian-notAtAll','asian-notWell', 'asian-veryWell', 'less-10', '10to15', '15to20', '20to25', '25to30', '30to35', '35to40', '40to45', '45to50', '50to60', '60to75', '75to100', '100to125', '125to150', '150to200', '200more']

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

	allTracts, tractAndPop = censusTracts.listTracts(app.cityID)
	#tract = app.cityID
	#For all the tracts in the specified city (county area), sum the number of people in the specified codes
	#Last paramter is 1, so that we get tract data (in the county)

	allTractsLatLng = fromFIPSlisttoLatLong.getLatLngFromFIPS(allTracts)

	iterator = 0
	length = len(allTracts)
	mapDistance = 1.5 / length


	while not displayingSomething:

		for tract in allTracts:
			#Get lat long of tract
			z = 16
			

			if tract is app.cityID or (lat - mapDistance < float(allTractsLatLng[iterator][0]) < lat + mapDistance and lng - mapDistance < float(allTractsLatLng[iterator][1]) < lng + mapDistance):
				displayingSomething = True
				#Get ACS data
				if len(app.genders) > 0: 
					if len(app.acsCodes) - len(app.genders) > 0: 
						ACSdata = getACS.getACSdata(tract, app.acsCodes)
				elif len(app.acsCodes) > 0: 
					ACSdata = getACS.getACSdata(tract, app.acsCodes)

				data, tempBlockAndPop = newGetPopDict.getpop(newKeys, tract, 2)
				#Add dictionary of blocks with total population to dictionary block adn Pop
				blockAndPop.update(tempBlockAndPop)

				#JUST ADDED
				
				#For every block in the current tract, get lat and long
				for item in data:
					blockFIPS = tract[0:11] +  item

					if blockFIPS not in listofFips:
						blockGroupIndex = blockFIPS[11:12]
						listofFips.append(blockFIPS)
						try: 
							acsSum = 0
							for element in ACSdata[1][int(blockGroupIndex)-1]:
								acsSum = acsSum + int(element)
							AcsDict[int(blockFIPS)] = acsSum
						except NameError: 
							pass	
						ValueDict[int(blockFIPS)] = data[item]

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

		mapDistance = mapDistance + 0.01
		iterator = 0

			#print FipsPixelDict
	for k,v in FipsPixelDict.iteritems():
		intermediate =  pixelcoordinates.getblockcoor(v, k[0], k[1], z)
		if len(intermediate.keys()) > 1:
			for k2, v2 in intermediate.iteritems():
				MegaDict[k2] = v2
		else:
			k2 = intermediate.keys()[0]
			v2 = intermediate.values()[0]
			MegaDict[k2] = v2

	#Iterate through listofValues and listofAcsValues to convert them to a shadeValue

	valueMax = float(max(ValueDict.values()))
	for key, value in ValueDict.iteritems():
		#value2 = TotalDict[key]
		if value / valueMax < 0.1: 
			shade = 0.1
		else: 
			shade = value / valueMax
		"""
		if value / value2 < 0.1:
			percentshade = 0.1
		else: 
			percentshade = value / value2 """
		if len(AcsDict.values()) > 0:
			MegaDict[key] = [MegaDict[key], ValueDict[key], AcsDict[key], shade]
		else:
			MegaDict[key] = [MegaDict[key], ValueDict[key], shade]


	businesses = []
	if len(request.form.get('business')) is not 0:
		businesses = scrapeYelp.getAddresses([lat, lng], request.form.get('city'), request.form.get('business'), mapDistance)
		#print businesses

	# with open('megaDict.txt', 'wb') as handle:
 #  		pickle.dump(MegaDict, handle)
 #  	with open('latLngZ.txt', 'wb') as handle:
 #  		pickle.dump([lat, lng, z], handle)
 #  	with open('businesses.txt', 'wb') as handle:
 #  		pickle.dump(businesses, handle)


 	print tractAndPop
 	print blockAndPop


	return render_template("fixing.html", data = MegaDict, lat = lat, lng = lng, z = z, yelpData = businesses)

@app.route('/fromMainPage')
def loadExample():

	with open('megaDict.txt', 'rb') as handle:
		exampleMegaDict = pickle.loads(handle.read())
	with open('latLngZ.txt', 'rb') as handle:
		exampleLat, exampleLng, exampleZ = pickle.loads(handle.read())
	with open('businesses.txt', 'rb') as handle:
		exampleBusinesses = pickle.loads(handle.read())


	return render_template("fixing.html", data = exampleMegaDict, lat = exampleLat, lng = exampleLng, z = exampleZ, yelpData = exampleBusinesses)


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