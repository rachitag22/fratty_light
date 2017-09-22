import os
from flask import Flask, request
from flask import render_template
from flask import g
from flask import redirect
from config import *
import hmac
import hashlib
import time
import sqlite3
import json
import requests
import pandas as pd

app = Flask(__name__)
data = 0
data_found = False

def setup_database():
	global DATABASE
	global conn
	global cursor
	DATABASE = "database.db"
	conn = sqlite3.connect(DATABASE)
	cursor = conn.cursor()

	create_table = "CREATE TABLE IF NOT EXISTS pnms (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT NOT NULL, email TEXT NOT NULL, phonenum TEXT NOT NULL, credits_completed BOOLEAN NOT NULL, status TEXT DEFAULT 'RUSH')"
	conn.execute(create_table)

	cursor.close()

setup_database()

@app.route("/", methods=["GET", "POST"])
def main():
	global data

	if (data_found):
		pnm_data = data.to_html()
	else:
		pnm_data = None
	return render_template("html/index.html", pnm_data=pnm_data)

@app.route("/rush-sign-up", methods=["GET", "POST"])
def rush_sign_up():
	return render_template("html/rush-sign-up.html")

@app.route('/upload', methods=["POST"])
def upload():
	global data, data_found

	# Input file
	file = request.files['file']
	if not file:
		return "Error: No file!"

	# Put input file in dataframe
	data = pd.read_csv(file, encoding='cp1252')


	data_found = True

	print(data)

	return main()

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), use_reloader=False)

