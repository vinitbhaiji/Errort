import tensorflow as tf
# vplatetype/model.keras
model = tf.keras.models.load_model('C:/VSCODE/EOL_LINE/Errort/vbandtype/model.keras')
import cv2
import numpy as np

# image=cv2.imread('leyparts5.jpg')
def banddetector(image):
    frame=cv2.resize(image, (100, 100))
    img_pred=frame
    img_pred=np.expand_dims(img_pred, axis=0)
    result=model.predict(img_pred)

    if result[0][0]> result[0][1]:
        return "notok"
    else :
        return "ok"

# image=cv2.imread('vband14.jpg')
# print(banddetector(image))