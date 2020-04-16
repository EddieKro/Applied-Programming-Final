import numpy as np
import flask
from flask import Flask, request
from symptoms_model.symptoms_covid import Symptoms
from xray_model.xray_covid_nn import NN_model
import os
import requests

app = Flask(__name__)
symptoms_model = Symptoms().load_model()
nn_model = NN_model()


@app.route('/app/health')
def health():
    return {'status': 'ok'}


@app.route('/symptoms/predict', methods=['POST'])
def syms_covid_prediction():
    data = flask.request.get_json(force=True)
    inputs = np.array(data['symptoms']).reshape(1,-1)
    preds = symptoms_model.predict(inputs)[0]
    if preds == 0:
        msg = f" probably don't have COVID-19 right now. Be careful, stay home, everything will be fine!"
    else:
        msg = f" should contact your doctor to get yourself tested. Please, don't panic and follow official instructions"
    
    message = f"Looks like your symptoms are{'n`t' if preds==0 else ''} severe. You" + msg
    data = {"message": message, "chat_id": data["chat_id"], "pred":int(preds)}
    requests.post(os.getenv('Message_resp_url'), json=flask.jsonify(data))
    return {'status': 'ok'}
    
    
if __name__ == '__main__':
    app.run('0.0.0.0', 8181,debug=True)
