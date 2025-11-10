from flask import Flask, request, jsonify
from flask_cors import CORS
from tensorflow.keras.models import load_model
import numpy as np
from PIL import Image
import io
import base64

app = Flask(__name__)
CORS(app)

model = load_model('model/model.keras')
emotion_labels = ['Angry', 'Disgust', 'Fear', 'Happy', 'Sad', 'Surprise', 'Neutral']

@app.route('/predict', methods=['POST'])
def predict():
  # get image
  data = request.get_json()
  image = data['image']

  image_data = image.split(',')[1] # remove base 64 header from image string
  image_bytes = base64.b64decode(image_data) # convert string back into bytes
  img = Image.open(io.BytesIO(image_bytes)).convert('L').resize((48, 48)) # resize image to 48x48px and convert to grayscale for model
  arr = np.array(img).astype('float32') / 255.0 # normalize values
  arr = np.expand_dims(arr, axis=(0, -1)) # add extra dimensions to match model shape=(1, 48, 48, 1)
  
  # run prediction
  prediction = model.predict(arr)

  label = emotion_labels[np.argmax(prediction)]
  confidence = float(np.max(prediction))

  return jsonify({'emotion': label, 'confidence': confidence})

@app.route('/')
def home():
  return '<p>Hello World!</p>'

if __name__=='__main__':
  app.run(host='0.0.0.0', port=5000)
