from flask import Flask, render_template, request,jsonify
from flask_sqlalchemy import SQLAlchemy
import os,pytesseract
from cv2 import cv2
from PIL import Image
import speech_recognition as sr
from gtts import gTTS  #it will record our audio
import random 
import playsound #it will play instantly not opening our default player
import time 
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract'

app = Flask(__name__)

"""
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///images.db'
db = SQLAlchemy(app)
class Images(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(300))
    data = db.Column(db.LargeBinary)
"""

UPLOAD_FOLDER = os.path.basename('./static')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#AUDIO_FOLDER = os.path.basename('./audio')
#app.config['UPLOAD_FOLDER'] = AUDIO_FOLDER


@app.route("/")
def main():
	return render_template('main.html')
def lucy_speak(audio_string):
    tts = gTTS(audio_string,lang='en')
    r = random.randint(1,1000000)
    
    audio_file = 'audio_'+str(r)+'.mp3'
    tts.save(audio_file)
    playsound.playsound(audio_file)
    print(audio_string)
    os.remove(audio_file)

@app.route("/upload", methods=['POST', 'GET'])
def upload():
    img = request.files['pic']
        
    """
    new_image = Images(name=img.filename, data=img.read())
    db.session.add(new_image)
    db.session.commit()
    return "Saved " + img.filename + " to the Database"
    """

    f = os.path.join(app.config['UPLOAD_FOLDER'], img.filename)
    img.save(f)
    saved_image = UPLOAD_FOLDER+"/"+img.filename
    image = cv2.imread(saved_image)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    preprocess = request.form["preprocess"]
    if  preprocess == "thresh":
        gray = cv2.threshold(gray, 0, 255,
                             cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]


    elif preprocess == "blur":
        gray = cv2.medianBlur(gray, 3)
   

    filename = "static/{}.png".format(os.getpid())
    cv2.imwrite(filename, gray)

    text = pytesseract.image_to_string(Image.open(filename))
    time.sleep(3)
    lucy_speak(text)
    return render_template('text.html', text=text, filename=saved_image)
    
    

if __name__ == '__main__':
	app.run(debug=True)