import tensorflow as tf
from tensorflow.keras.models import Model
from tensorflow.keras.applications import VGG16
from tensorflow.keras.layers import Input, AveragePooling2D, Dropout 
from tensorflow.keras.layers import Flatten, Dense 
import cv2
import numpy as np

class NN_model:
    def __init__(self):
        self.img_shape = (224, 224, 3)

    def init_model(self):
        baseModel = VGG16(weights="imagenet", include_top=False, 
            input_tensor=Input(shape=self.img_shape))
        headModel = baseModel.output
        headModel = AveragePooling2D(pool_size=(4, 4))(headModel)
        headModel = Flatten(name="flatten")(headModel)
        headModel = Dense(64, activation="relu")(headModel)
        headModel = Dropout(0.5)(headModel)
        headModel = Dense(2, activation="softmax")(headModel)
    
        model = Model(inputs=baseModel.input, outputs=headModel)
        return model
    
    def image_preprocessing(self, img):
        img = np.array(img, dtype=np.uint8)
        img = cv2.cvtColor(cv2.UMat(img), cv2.COLOR_BGR2RGB)
        img = cv2.resize(img, (224, 224))
        img = img / 255.0
        img = np.array(img)
        img = np.expand_dims(img, axis=0)
        return img
    
    def predict(self, image):
        sample = self.image_preprocessing(image)
        model = self.init_model()
        model.load_weights('./covid19.model')
        preds = model.predict(sample)
        class_pred = np.argmax(preds)
        return class_pred, preds[0][class_pred]
