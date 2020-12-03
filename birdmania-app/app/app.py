# Standard modules
import base64
from datetime import datetime
import json
import os
import requests

# Open source modules
from flask import Flask, make_response, render_template, request, redirect, url_for, session
import pywebaudioplayer as pwa

# Project modules
import model 
import s3_utils

app = Flask(__name__)
APP_ROOT = os.path.dirname(os.path.abspath(__file__))
app.config['UPLOAD_FOLDER'] = os.path.join(APP_ROOT, 'uploads')
app.config["BUCKET"]  =  "2020-grads-tech-assignment-birdmania-bucket"
app.config["AUDIO"] = "birdsong-recognition/birds_recordings_uploaded/"
# Set the secret key to some random bytes. 
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'

@app.route("/")
def index():	
	return render_template("index.html")

@app.route('/', methods=['POST'])
def upload_file():
	if request.method=='POST':
		# Get file
		uploaded_file = request.files['file']
		if uploaded_file.filename != '':
			# Get location 
			location = request.form.get('location')
			# Get date
			date = request.form.get('date')
			# Get username
			user = session.get('username')
			# Rename file
			filename = rename_file(uploaded_file)
			session['filename'] = filename
			# Identify bird specie
			prediction = model.predict('static/uploads/' + filename)			
			session['prediction'] = prediction[0]
			session['image_prediction'] = prediction[1]
			# Upload file to s3
			#s3_utils.upload_file_to_s3('static/uploads/' + filename, app.config["BUCKET"], app.config["AUDIO"] + filename)
		return redirect("/result")
	return (redirect('/'))

@app.route("/result",methods=['GET'])
def result():
	# Prediction to display
	to_print = "The bird is " + session.get('prediction')
	# Image to visualize
	image = 'static/species_images/' + session.get('image_prediction')
	# Build wave to visualize
	wave = pwa.wavesurfer('static/uploads/' + session.get('filename'), controls={'text_controls': False, 'backward_button': True, 'forward_button': True, 'mute_button': False},
				display={'unplayed_wave_colour': 'darkorange', 'played_wave_colour': 'purple', 'height': 56, 'background_colour': None},
				behaviour={'mono': False})
	return render_template("main.html", message=to_print, picture=image, audio=wave)

@app.route("/about",methods=['GET'])
def about():
	return render_template("about.html")

def rename_file(uploaded_file):
	extension = uploaded_file.filename.rsplit('.', 1)[1].lower()
	uploaded_file.filename = str(datetime.now()) + '.' + extension
	uploaded_file.save('static/uploads/' + uploaded_file.filename)
	return uploaded_file.filename

if __name__ == '__main__':
	app.run(host='0.0.0.0', port=5000, debug=True)
