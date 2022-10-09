from msilib.schema import Class
import flask
from flask import Flask, render_template, request
import os
from tensorflow import keras

from keras.models import load_model 
from keras.preprocessing import image
import numpy as np

import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow

from flask import Flask,render_template, redirect, url_for, request, jsonify
from flask_mysqldb import MySQL

import cv2 as cv2
img_size=(50, 50)
classes=['Ahmed Amr', 'Ali Habib', 'Mohamed Bebo', 'Mohamed Labib', 'Mohamed Mokhtar']

img_path=r"160.jpg"

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'aadhar'
mysql = MySQL(app)



model = load_model(r'EfficientNetB3-iris-0.78.h5')

@app.route('/', methods=['GET'])
def home():
  return render_template('index.html',user_image=img_path)

@app.route('/', methods=['POST'])
def predict():
  # predicting images
  img=plt.imread(img_path)
  print("hello")
  imagefile = request.files['imagefile']
  img=cv2.resize(img, img_size)
  plt.axis('off')
  plt.imshow(img)
  img=np.expand_dims(img, axis=0)
  #image_path = './static/images/' + imagefile.filename 
  imagefile.save(img_path)

  #img = image.load_img(img_path, target_size=(300, 300))
  #x = image.img_to_array(img)
  #x = np.expand_dims(x, axis=0)

  #images = np.vstack([x])
  pred=model.predict(img)
  index=np.argmax(pred[0])
  kclass=classes[index]
  #classes = model.predict(images, batch_size=10)

#   pic = os.path.join(app.config['UPLOAD_FOLDER'], imagefile.filename)
  
  #if classes[0]>0.5:
  cur = mysql.connection.cursor() 
  print("Succesfull")
  cur.execute("SELECT Aadhar_Number FROM niris WHERE Name = %s", (kclass,))
  user = cur.fetchone()
  cur.execute("SELECT Status FROM vaccination WHERE Aadhar_Number = %s", (user,))
  user1=cur.fetchone()
  return render_template('index.html', user_image=img_path, prediction_text='Name: {}'.format(kclass),user=user,user1=user1)
  #else:
    #return render_template('index.html', user_image=pic, prediction_text='{} is the image of Horse'.format(imagefile.filename))



if __name__=='__main__':
  app.run(host='localhost', port=5000)