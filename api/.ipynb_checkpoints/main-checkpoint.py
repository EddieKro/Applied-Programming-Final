import urllib
import shutil
import cv2
import sys
import numpy as np
from PIL import Image
from flask import Flask, request
from xray_model.xray_covid_nn import NN_model
from symptoms_model import symptoms_covid

app = Flask(__name__)

@app.route('/app/health')
def health():
	return {'status': 'ok'}

@app.route('/app/symptoms_predict', methods=['GET', 'POST'])
def covid_symptoms_prediction():
    s_model = symptoms_covid()
    clf = s_model.load_model()
    symptoms = s_model.symptoms()
    preds = clf.predict(symptoms)
    return {'pred_proba':preds}

@app.route('/symptoms/predict', methods=['POST'])
def syms_covid_prediction():
	inputs = flask.request.get_json(force=True)
    
    
	preds = model.predict(inputs)
	message = f"You should call an ambulance! You probably have COVID-19."
	requests.post(os.getenv('Message_resp_url'), json={"message": message, "chat_id": inputs["chat_id"]})



# takes image as url. 
@app.route('/app/download', methods=['GET'])
def image_covid_prediction():
	url = str(request.args['url'])
	print(url, file=sys.stderr)
	url_response = urllib.request.urlopen(url)
	img_array = np.array(bytearray(url_response.read()), dtype=np.uint8)
	nn_model = NN_model()
	preds = nn_model.predict(img_array)
	return {'pred_class':str(preds[0]), 'class_prob':str(preds[1])}

if __name__ == '__main__':
	app.run('0.0.0.0', 8181)
