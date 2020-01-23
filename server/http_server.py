from flask import Flask, json, request
import sys
sys.path.insert(0, '..')
from tools.json_abs import *
import leveldata


app = Flask(__name__)


@app.route('/upload', methods=['POST'])
def post_upload():
	if request.method == 'POST':
		