# root init 
from flask import Flask, render_template
app = Flask("pitho")
app.secret_key = "xylsanity"
app.debug = True
from pitho.controllers import *
"""@app.route('/')
def home():
	name = "database"
	return render_template("home.html", data = name)
@app.route('/about')
def about():
	return render_template("about.html")
@app.route('/contact')
def contact():
	return render_template("contact.html")"""