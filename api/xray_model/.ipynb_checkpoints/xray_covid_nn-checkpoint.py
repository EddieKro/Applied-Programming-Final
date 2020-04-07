import cv2
import numpy as np
from PIL import Image
import matplotlib.pyplot as plt
from tensorflow.keras.models import Model
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input, AveragePooling2D, Dropout 
from tensorflow.keras.layers import Flatten, Dense  

class NN_model:
    def __init__(self):
        self.img_shape = [224, 224, 3]

    def init_model(self, in_shape):
        baseModel = VGG16(weights="imagenet", include_top=False, 
            input_tensor=Input(shape=(in_shape[0], in_shape[1], 
                in_shape[2])))
        headModel = baseModel.output
        headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
        headModel = Flatten(name="flatten")(headModel)
        headModel = Dense(64, activation="relu")(headModel)
        headModel = Dropout(0.5)(headModel)
        headModel = Dense(2, activation="softmax")(headModel)
    
        model = Model(inputs=baseModel.input, outputs=headModel)
        return model
    
    def image_download_preprocessing(self, np_img, check=False):
        if check:
            img= cv2.imread(np_img)
        else :
            img = cv2.imdecode(np_img, -1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict(self, sample, check=False):
        sample = self.image_download_preprocessing(sample, check)
        model = self.init_model(in_shape = self.img_shape)
        model.load_weights('xray_model/covid19.model')
        preds = model.predict(sample)
        class_pred = np.argmax(preds)
        return class_pred, preds[0][class_pred]

if __name__ == '__main__':
    mod = NN_model()
    img = Image.open('test.jpeg')
    img = np.asarray(img)
    preds = mod.predict('test.jpeg', check=True)
    print(preds)