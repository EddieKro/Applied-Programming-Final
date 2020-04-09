import numpy as np 

from joblib import load
from sklearn.linear_model import RidgeClassifier

class Symptoms:
    def load_model(self):
        clf = load('symptoms_model/model.joblib')
        return clf
    
    @staticmethod
    def preprocess_symptoms(response):
        symptoms = np.random.randint(0,2,(1,24))
        return symptoms
    
# if __name__ == '__main__':
#     clf = load('model.joblib')
    