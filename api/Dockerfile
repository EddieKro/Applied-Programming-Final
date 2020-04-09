FROM tensorflow/tensorflow:1.15.0-py3
WORKDIR /app
COPY . ./
RUN pip3 install -r requirements.txt
RUN apt-get install -y libsm6 libxext6 libxrender-dev
ENTRYPOINT ["python", "server.py"]
