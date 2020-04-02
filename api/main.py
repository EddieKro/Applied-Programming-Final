import urllib
import shutil
import cv2
import sys
import numpy as np
from PIL import Image
from flask import Flask, request
from xray_model.xray_covid_nn import NN_model

app = Flask(__name__)

@app.route('/app/health')
def health():
	return {'status': 'ok'}

#@app.route('/app/symptoms_predict', methods=['GET', 'POST'])
#def covid_symptoms_prediction():
	## get symptoms list

#	tree_model = Tree_model()
#	preds = tree_model.predict(symptoms)
#	return {'pred_proba':preds}


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
