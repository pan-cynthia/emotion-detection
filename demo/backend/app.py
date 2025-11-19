import base64
import io
import os

import cv2
import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app, resources={r'/*': {'origins': '*'}})

# load pretrained opencv face detector
face_classifier = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

model = load_model('model/model.keras')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

def preprocess_image(img):
  '''
  Detects the largest face in an image using OpenCV's Haar cascade
  and preprocesses it for model prediction.

  Args:
    img: The input image.

  Returns:
    np.ndarray: Preprocessed image ready for model prediction with shape (1, 48, 48, 1).
  '''

  img = np.array(img)

  # convert image to grayscale and resize to match model input
  gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
  faces = face_classifier.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5)

  if len(faces) == 0:
    # no face detected, fallback to full image
    face = cv2.resize(gray, (48, 48))
  else:
    # choose largest face in image
    max_area = 0
    largest_face = None
    for (x, y, w, h) in faces:
      area = w * h
      if area > max_area:
        max_area = area
        largest_face = (x, y, w, h)
    
    x, y, w, h = largest_face
    face = gray[y:y+h, x:x+w]
    face = cv2.resize(face, (48, 48))

  # reshape values for model input (1, 48, 48, 1)
  arr = face.astype('float32')
  arr = np.expand_dims(arr, axis=(0, -1))

  return arr

@app.route('/predict', methods=['POST'])
def predict():
  '''
  Handles emotion prediction requests from the frontend.

  Expects a JSON payload containing a base64 encoded image string.
  The image is decoded, converted to grayscale, and resized to 48x48 pixels
  using face detection before being passed into the trained model for prediction.

  Returns:
    JSON: A response containing:
      - 'emotion' (str): The predicted emotion label from ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'].
      - 'confidence' (float): The model's confidence score (0.0 - 1.0) for the predicted emotion.
  '''

  # get image
  data = request.get_json()
  image = data['image']

  # remove base64 header and decode image bytes
  image_data = image.split(',')[1]
  image_bytes = base64.b64decode(image_data)

  # load image
  img = Image.open(io.BytesIO(image_bytes)).convert('RGB')

  # preprocess with face detection
  arr = preprocess_image(img)

  # run prediction and extract highest confidence emotion
  prediction = model.predict(arr)
  label = emotion_labels[np.argmax(prediction)]
  confidence = float(np.max(prediction))

  return jsonify({'emotion': label, 'confidence': confidence})

@app.route('/')
def home():
  return '<p>Emotion Detection Backend is Running!</p>'

if __name__=='__main__':
  port = int(os.environ.get("PORT", 5000))
  app.run(host='0.0.0.0', port=port)
