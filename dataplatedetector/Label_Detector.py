import tensorflow as tf
# dataplatedetector/model.keras
model = tf.keras.models.load_model('C:\VSCODE\EOL_LINE\Errort\dataplatedetector\model.keras')
import cv2
import numpy as np

def dataplate(image):
    frame=cv2.resize(image, (100, 100))
    img_pred=frame
    img_pred=np.expand_dims(img_pred, axis=0)
    result=model.predict(img_pred)

    if result[0][0]> result[0][1]:
        return "wrong"
    else :
        return "right"

# input_image=cv2.imread('dp4.jpg')
# print(dataplate(input_image))