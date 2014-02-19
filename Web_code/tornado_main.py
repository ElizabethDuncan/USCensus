# Access this webpage from a browser at url: http://127.0.0.1:8888/

from flask import *
import json

app = Flask(__name__)
app.debug = True
app.vars = {}

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
	app.vars['race'] = request.form.get('race')
	app.vars['gender'] = request.form.get('gender')
	app.vars['age'] = request.form.get('age')

	f = open('data.txt' ,'w')
	f.write('race: %s\n' %(app.vars['race']))
	f.write('gender: %s\n' %(app.vars['gender']))
	f.write('age: %s\n' %(app.vars['age']))
	f.close()

	#Find a code matching race, gender, and age

	#With the code, call Marena's python script
	data = app.vars['race']

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