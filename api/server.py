import numpy as np
import flask
from flask import Flask, request
from xray_model.xray_covid_nn import NN_model
import os

app = Flask(__name__)
model = NN_model()

@app.route('/app/health')
def health():
	return {'status': 'ok'}

# takes image as url.
@app.route('/xray/predict', methods=['POST'])
def image_covid_prediction():
	inputs = flask.request.get_json(force=True)
	preds = model.predict(inputs["image"])
	message = f"You have a {preds[1]*100:.2f}% chance of {'not ' if preds[0]==0 else ''}having COVID-19."
	request.post(os.getenv('Message_resp_url'), json={"message": message, "chat_id": inputs["chat_id"]})

if __name__ == '__main__':
	app.run('0.0.0.0', 8181)
