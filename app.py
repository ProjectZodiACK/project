from flask import Flask, render_template, request
from flask_autoindex import AutoIndex # file directory index for upload history
from werkzeug.utils import secure_filename
import os
import os.path
import datetime # used to date the folders for uploads
import time 
import sys
from PIL import Image
import pytesseract # OCR
import argparse
import cv2 # OCR
import subprocess
import vig_decryption # vingenere cipher
import func_timeout # time out the decryption processes if it hasn't returned an answer
import solitaire # solitaire cipher
import caesar # casear sipher
from textblob import TextBlob # language translation
from loguru import logger # logger

__author__ = 'Original Code by Rick Torzynski <ricktorzynski@gmail.com> & Modified by IST 440W - Team 1 FA2022'
__source__ = 'https://github.com/ProjectZodiACK/'

app = Flask(__name__)
# initialized the upload folder by date
UPLOAD_FOLDER = './static/uploads/' + datetime.datetime.now().strftime("%Y-%m-%d")
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER 
app.config['MAX_CONTENT_LENGTH'] = 10 * 1024 * 1024

idx = AutoIndex(app, './static/uploads', add_url_rules=False, template_context = dict(SITENAME = "ZodiACK Tool - IST 440W FA22"))

logger.remove()
logger.add(sys.stderr, format="{time:HH:mm:ss.SS} | {level} | {message}")
logger.add("./static/uploads/{time:YYYY-MM-DD}/daily-{time:YYYY-MM-DD}.log", rotation="00:00")

# index
@app.route("/")
def index():
  return render_template("index.html")

# about us page
@app.route("/about")
def about():
  return render_template("about.html")

#display file index for uploads 
@app.route("/history")
@app.route("/history/<path:path>")
@app.route("/logs")
@app.route("/logs/<path:path>")
def autoindex(path='.'):
    return idx.render_autoindex(path, template='history.html')

@app.route('/upload-file', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']

      # create a secure filename
      filename = secure_filename(f.filename)

      # create directory and save file to /static/uploads
      if not(os.path.exists(app.config['UPLOAD_FOLDER']) and os.path.isdir(app.config['UPLOAD_FOLDER'])):
        os.mkdir(app.config['UPLOAD_FOLDER'])
      logger.info("Processing Started")
      filepath = os.path.join(app.config['UPLOAD_FOLDER'],filename)
      f.save(filepath)
      logger.success("File successfully uploaded to: " + filepath)

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
      logger.success("File successfully converted with CV2: " + ofilename)
      
      # perform OCR on the processed image
      #text = pytesseract.image_to_string(Image.open(ofilename), config='--psm 7')
      
      cipherChoice = request.form['cipherChoice']
      logger.info("Cipher Chosen: " + cipherChoice)
      if cipherChoice == "cae":
        text = pytesseract.image_to_string(Image.open(ofilename), config='--psm 7')
        logger.info("Optical Character Recognition: " + text)
        dtext = caesar.main(text)
        logger.info("English Translation: " + dtext)
        tb = TextBlob(dtext)
        fr = tb.translate(from_lang='en', to='fr')
        logger.info("French Translation: " + str(fr))
        es = tb.translate(from_lang='en', to='es')
        logger.info("Spanish Translation: " + str(es))
        logger.success("Processing Complete")
        logger.disable("")
        return render_template("uploaded.html", encryptedtext=text, decryptedtext=dtext, fname=filepath, ofname=ofilename, esLang=es, frLang=fr)
      elif cipherChoice == "sol":
        text = pytesseract.image_to_string(Image.open(ofilename), config='--psm 7')
        logger.info("Optical Character Recognition: " + text)
        text = text.replace(' ','')
        dtext = solitaire.main(text)
        logger.info("English Translation: " + dtext)
        tb = TextBlob(dtext)
        fr = tb.translate(from_lang='en', to='fr')
        logger.info("French Translation: " + str(fr))
        es = tb.translate(from_lang='en', to='es')
        logger.info("Spanish Translation: " + str(es))
        logger.success("Processing Complete")
        logger.disable("")
        return render_template("uploaded.html", encryptedtext=text, decryptedtext=dtext, fname=filepath, ofname=ofilename, esLang=es, frLang=fr)
      elif cipherChoice == "vig":
        text = pytesseract.image_to_string(Image.open(ofilename), config='--psm 7')
        logger.info("Optical Character Recognition: " + text)
        dtext = str(vig_decryption.brute_force_decryption_vigenere(text, 95))
        logger.info("English Translation: " + dtext)
        tb = TextBlob(dtext)
        fr = tb.translate(from_lang='en', to='fr')
        logger.info("French Translation: " + str(fr))
        es = tb.translate(from_lang='en', to='es')
        logger.info("Spanish Translation: " + str(es))
        logger.success("Processing Complete")
        logger.disable("")
        return render_template("uploaded.html", encryptedtext=text, decryptedtext=dtext, fname=filepath, ofname=ofilename, esLang=es, frLang=fr)
      else: 
        text = pytesseract.image_to_string(Image.open(ofilename), config='--psm 7')
        logger.info("Optical Character Recognition: " + text)
        logger.exception("ERROR: Decryption Failed")
        logger.disable("")
        return render_template("uploaded.html", encryptedtext=text, decryptedtext="ERROR: Decryption Failed", fname=filepath, ofname=ofilename)

if __name__ == '__main__':
  port = int(os.environ.get('PORT', 5000))
  app.run(debug=True, host='0.0.0.0', port=port)
  # app.run(host="0.0.0.0", port=5000, debug=True)