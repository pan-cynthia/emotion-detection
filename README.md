# Emotion Detection

A real time emotion detection application using React for the frontend and Flask + Tensorflow + OpenCV for the backend. The model detects human faces and classifies emotions into one of seven categories: Angry, Disgust, Fear, Happy, Sad, Surprise, and Neutral.

Access a live demo [here](https://pan-cynthia.github.io/emotion-detection/).

## Note

The backend is hosted on a free Render service that goes to sleep when inactive.

If no data is showing up on the frontend (GitHub pages), please visit the backend once to wake it up: [Backend API](https://emotion-detection-ebqp.onrender.com/)

After ~30 seconds, refresh the frontend and it should display correctly.

## Prerequisites

[Docker](https://www.docker.com/products/docker-desktop) must be installed to build and run the backend and notebooks.

## Demo Application

To install and run the demo locally, follow these steps in your terminal:

### 1. Clone the repository

```bash
git clone https://github.com/pan-cynthia/emotion-detection.git
cd emotion-detection/demo
```

### 2. Install frontend dependencies

```bash
cd demo/frontend
npm install
```

### 3. Build the backend Docker image

From the `demo` directory:

```bash
docker build -t emotion-backend backend
```

### 4. Run the backend container

```bash
docker run -p 5000:5000 emotion-backend
```

Backend will be running at: http://localhost:5000

### 5. Run the frontend

In a new terminal:

```
cd frontend
npm run dev
```

Frontend will be running at: http://localhost:5173

## Model/Notebooks

This section contains the notebooks used to train and evaluate the CNN. The notebooks run inside a Docker container with Tensorflow and required dependencies pre-installed.

To install and run the notebooks locally, follow these steps in your terminal:

### 1. Clone the repository (if not already done)

```bash
git clone https://github.com/pan-cynthia/emotion-detection.git
```

### 2. Build the Docker image

```bash
docker build -t emotion-detection:latest .
```

### 3. Run the Docker container with notebook support

```bash
docker run -it -p 8888:8888 \
    -v ~/Documents/projects/emotion-detection:/tf/emotion-detection \
    emotion-detection:latest
```

When the container starts, Jupyter Notebook will output a message like this:

```kotlin
To access the server, open this file in a browser:
    file:///root/.local/share/jupyter/runtime/jpserver-1-open.html
Or copy and paste one of these URLs:
    http://127.0.0.1:8888/?token=<access_token_here>
```

Open the URL containing the token:
```ruby
http://127.0.0.1:8888/?token=<access_token_here>
```

This will launch the notebook environment.

---
