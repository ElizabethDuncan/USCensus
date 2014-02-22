# Access this webpage from a browser at url: http://127.0.0.1:8888/

from flask import *
import json

app = Flask(__name__)
app.debug = True
app.vars = {}
app.desired_demographics = []

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
	#f = open('test.txt' ,'w')
	#f.close()
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

	f = open('data.txt' ,'w')
	app.desired_demographics.append(request.form.get('city'))
	for demographic in app.vars:
		if app.vars[demographic] == 'True':
			#f.write(demographic + ': %s\n' %(app.vars[demographic]))
			app.desired_demographics.append(demographic)
	f.close()



	#Find a code matching race, gender, and age

	#With the code, call Marena's python script
	data = app.vars['gender Female']
	print app.desired_demographics
	app.vars = []

	#print the results in getsurveyresults.html

	return render_template("getsurveyresults.html", data=data)


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