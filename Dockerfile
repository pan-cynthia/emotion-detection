FROM tensorflow/tensorflow:2.19.0-jupyter

# set working directory
WORKDIR /tf/emotion-detection

# install python packages
RUN pip install --no-cache-dir \
numpy \
pandas \
matplotlib \
scikit-learn
