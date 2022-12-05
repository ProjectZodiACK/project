from flask import Flask, render_template, request
from flask_autoindex import AutoIndex
from werkzeug.utils import secure_filename
import os
import datetime
import time
import sys
from PIL import Image
import pytesseract
import argparse
import cv2
import subprocess
import vig_decryption
import func_timeout
import solitaire
import caesar

__author__ = 'Rick Torzynski <ricktorzynski@gmail.com>'
__source__ = ''

app = Flask(__name__)
UPLOAD_FOLDER = './static/uploads/' + datetime.datetime.now().strftime("%Y-%m-%d")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

@app.route("/")
def index():
  return render_template("index.html")

@app.route("/about")
def about():
  return render_template("about.html")

@app.route("/history")
def history():
  return render_template("history.html")

@app.route("/logs")
def logs():
  return render_template("logs.html")

@app.route('/upload-file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      # create a secure filename
      filename = secure_filename(f.filename)

      # create directory and save file to /static/uploads
      if not(os.path.exists(app.config['UPLOAD_FOLDER']) and os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.mkdir(app.config['UPLOAD_FOLDER'])
  
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)

      # load the example image and convert it to grayscale
      image = cv2.imread(filepath)
      gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
      
      # apply thresholding to preprocess the image
      gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]

      # apply median blurring to remove any blurring
      gray = cv2.medianBlur(gray, 3)

      # save the processed image in the /static/uploads directory
      ofilename = os.path.join(app.config['UPLOAD_FOLDER'],"{}.png".format(os.getpid()))
      cv2.imwrite(ofilename, gray)
      
      # perform OCR on the processed image
      text = pytesseract.image_to_string(Image.open(ofilename))
      
      # remove the processed image
      os.remove(ofilename)

      return render_template("uploaded.html", displaytext=text, fname=filepath)

@app.route('/upload-solitaire', methods = ['GET', 'POST'])
def upload_solitaire():
   if request.method == 'POST':
      s = request.form['text']
      s = s.replace(' ','')

      # create directory and save file to /static/uploads
      if not(os.path.exists(app.config['UPLOAD_FOLDER']) and os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.mkdir(app.config['UPLOAD_FOLDER'])
      
      return render_template("uploaded.html", displaytext=solitaire.main(s))

@app.route('/upload-vigenere', methods = ['GET', 'POST'])
def upload_vigenere():
   if request.method == 'POST':
      f = request.form['text']

      # create directory and save file to /static/uploads
      if not(os.path.exists(app.config['UPLOAD_FOLDER']) and os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.mkdir(app.config['UPLOAD_FOLDER'])
  
      return render_template("uploaded.html", displaytext=vig_decryption.brute_force_decryption_vigenere(f, 100))

@app.route('/upload-caesar', methods = ['GET', 'POST'])
def upload_caesar():
   if request.method == 'POST':
      f = request.form['text']

      # create directory and save file to /static/uploads
      if not(os.path.exists(app.config['UPLOAD_FOLDER']) and os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.mkdir(app.config['UPLOAD_FOLDER'])
  
      return render_template("uploaded.html", displaytext=caesar.main(f))

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)
  # app.run(host="0.0.0.0", port=5000, debug=True)