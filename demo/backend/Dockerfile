FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

COPY . .

# install system dependencies for opencv
RUN apt-get update && apt-get install -y libgl1 libglib2.0-0 && rm -rf /var/lib/apt/lists/*

# install python dependencies
RUN pip install --no-cache-dir --ignore-installed flask flask-cors pillow opencv-python-headless

EXPOSE 5000
CMD [ "python", "app.py" ]
