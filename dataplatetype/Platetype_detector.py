import tensorflow as tf
model = tf.keras.models.load_model('C:\VSCODE\EOL_LINE\Errort\dataplatetype\model.keras')
import cv2
import numpy as np

# image=cv2.imread('leyparts5.jpg')
def datareader(image):
    frame=cv2.resize(image, (100, 100))
    img_pred=frame
    img_pred=np.expand_dims(img_pred, axis=0)
    result=model.predict(img_pred)

    if result[0][0]> result[0][1] and result[0][0]>result[0][2]:
        return "Eicher"
    elif result[0][1]> result[0][0] and result[0][1]>result[0][2] :
        return "Holset"
    else :
        return "Leyparts"

