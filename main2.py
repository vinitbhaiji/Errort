from ultralytics import YOLO
from vbandtype import Vband_Detector
from dataplatedetector import Label_Detector
from dataplatetype import Platetype_detector
from snappin import snap_detector
import cv2 
import math
import cvzone
import numpy as np

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

def detectioncamera(frame):
    model = YOLO("C:/VSCODE/EOL_LINE/Errort/best.pt")
    results=model.predict(frame)
    result=results[0]
    output=[]
    for box in result.boxes:
        x1,y1,x2,y2=[
            round(x) for x in box.xyxy[0].tolist()
        ]
        cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,255),2)
        frame1=frame[x1:x2,y1:y2]
        class_id=box.cls[0].item()
        cvzone.putTextRect(frame,f'{result.names[class_id]}',(x1,y1),1,2)
        if result.names[class_id]=="vband":
            if(Vband_Detector.banddetector(frame1)=='ok'):
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                cvzone.putTextRect(frame,"OK",(x1,y1),1,2)
                print("Vband is correct")
            else :
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cvzone.putTextRect(frame,"NOT OK",(x1,y1),1,2)
                print("Vband is not correct")
        
        if result.names[class_id]=="dataplate":
            if(Label_Detector.dataplate(frame1)=="wrong"):
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cvzone.putTextRect(frame,"Not Ok",(x1,y1),1,2)
                print("Data Plate wrongly placed")
            else :
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                print("Data Plate correctly placed")
                datatype=Platetype_detector.datareader(frame1)
                print("Type of data plate : ",datatype)
                cvzone.putTextRect(frame,f'{datatype}',(x1,y1),1,2)
        
        if result.names[class_id]=="snappin":
            if(snap_detector.snappin(frame)=="wrong"):
                print("Snap-Pin wrongly attached")
            else :
                print("Snap-Pin correctly attached") 

        output.append(result.names[class_id])
            # prob = round(box.conf[0].item(), 2)
            # output.append([
            # x1, y1, x2, y2, result.names[class_id], prob
            # ])
    cv2.imshow('Image',frame)
    cv2.waitKey(0)


input_image=cv2.imread('tc4.jpg')
detectioncamera(input_image)
