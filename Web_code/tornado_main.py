# Access this webpage from a browser at url: http://127.0.0.1:8888/

from flask import *
import json

app = Flask(__name__)
app.debug = True

@app.route("/")
def index():
	return render_template("index.html")
"""
@app.route("/design")
def design():
	return render_template("design.html")

@app.route("/timeline")
def timeline():
	return render_template("timeline.html")

@app.route("/reflection")
def reflection():
	return render_template("reflection.html")

@app.route("/team")
def team():
	json_team_data = open("data/team.json")
	team_data = json.load(json_team_data)
	json_team_data.close()
	return render_template("team.html", team=team_data)
	"""

if __name__ == "__main__":
	app.run()