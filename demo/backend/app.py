import base64
import io

import numpy as np
from flask import Flask, jsonify, request
from flask_cors import CORS
from PIL import Image
from tensorflow.keras.models import load_model

app = Flask(__name__)
CORS(app)

model = load_model('model/model.keras')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

@app.route('/predict', methods=['POST'])
def predict():
  '''
  Handles emotion prediction requests from the frontend.

  Expects a JSON payload containing a base64 encoded image string.
  The image is decoded, converted to grayscale, resized to 48x48 pixels, and normalized
  before being passed into the trained model for prediction.

  Returns:
    JSON: A response containing:
      - 'emotion' (str): The predicted emotion label from ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral'].
      - 'confidence' (float): The model's confidence score (0.0 - 1.0) for the predicted emotion.
  '''

  # get image
  data = request.get_json()
  image = data['image']

  # process image by removing base64 header and decoding image bytes
  image_data = image.split(',')[1]
  image_bytes = base64.b64decode(image_data)

  # convert image to grayscale and resize to match model input
  img = Image.open(io.BytesIO(image_bytes)).convert('L').resize((48, 48))

  # reshape values for model input (1, 48, 48, 1)
  arr = np.array(img).astype('float32')
  arr = np.expand_dims(arr, axis=(0, -1))
  
  # run prediction
  prediction = model.predict(arr)

  # extract highest confidence emotion
  label = emotion_labels[np.argmax(prediction)]
  confidence = float(np.max(prediction))

  return jsonify({'emotion': label, 'confidence': confidence})

@app.route('/')
def home():
  return '<p>Hello World!</p>'

if __name__=='__main__':
  app.run(host='0.0.0.0', port=5000)
