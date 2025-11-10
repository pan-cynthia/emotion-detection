FROM tensorflow/tensorflow:2.19.0

WORKDIR /app

COPY . .

RUN pip install --no-cache-dir --ignore-installed flask flask-cors pillow

EXPOSE 5000
CMD [ "python", "app.py" ]
