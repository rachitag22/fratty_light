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

@app.route("/", methods=['GET', 'POST'])
def main():
	return render_template('index.html')

@app.route('/upload', methods=["POST"])
def upload():
	
	# Input file
	file = request.files['file']
	if not file:
		return "Error: No file!"

	# Put input file in dataframe
	data = pd.read_csv(file, encoding='cp1252')

	print(data)

	return render_template('index.html')

app.run(host=os.getenv('IP', '0.0.0.0'), port=int(os.getenv('PORT', 8080)), use_reloader=False)