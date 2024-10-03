from flask import Flask,render_template,Response,request, jsonify
from asyncio import streams
from ultralytics import YOLO
from vbandtype import Vband_Detector
from dataplatedetector import Label_Detector
from dataplatetype import Platetype_detector
from snappin import snap_detector
import cv2 
import datetime
import math
import cvzone
import numpy as np
import pandas as pd
import cv2
import save_db

app=Flask(__name__)



model = YOLO("D:\Downloads\Cummins\EOL_CUMMINS\EOL_LINE\Errort\best.pt")

def unique(list1):
    x = np.array(list1)
    return np.unique(x)

flag=0
i=0
j=0
k=0
check_value=0
list_dict={1:[0,0,0,0,0,0,0],2:[0,0,0,0,0,0,0]}
def detection(frame):
    global flag,i,j,k
    global check_value
    check=False
    if flag==3:
        check=True

    if flag==1:
        x=i
    elif flag==2:
        x=j
    elif flag==3:
        x=k

    flag=0
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
                list_dict[x][6]=1
                print("Vband is correct")
            else :
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cvzone.putTextRect(frame,"NOT OK",(x1,y1),1,2)
                print("Vband is not correct")
        
        if result.names[class_id]=="dataplate":
            if(Label_Detector.dataplate(frame)=="wrong"):
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,0,255),2)
                cvzone.putTextRect(frame,"Not Ok",(x1,y1),1,2)
                print("Data Plate wrongly placed")
            else :
                cv2.rectangle(frame,(x1,y1),(x2,y2),(0,255,0),2)
                print("Data Plate correctly placed")
                list_dict[x][0]=1
                list_dict[x][1]=1
                list_dict[x][2]=1
                datatype=Platetype_detector.datareader(frame1)
                print("Type of data plate : ",datatype)
                cvzone.putTextRect(frame,f'{datatype}',(x1,y1),1,2)
        
        if result.names[class_id]=="snappin":
            if(snap_detector.snappin(frame)=="wrong"):
                print("Snap-Pin wrongly attached")
            else :
                list_dict[x][3]=1
                print("Snap-Pin correctly attached")
                
        if result.names[class_id]=='endlink':
            list_dict[x][4]=1
            print("Endlink is present")
        
        if result.names[class_id]=='hoseclip':
            list_dict[x][5]=1
            print("Hoseclip is correctly attached")

        output.append(result.names[class_id])

    if(check==True):
        char="OK"
        check_value=1
        for y in range(7):
            if list_dict[x][y]==0:
                char="NOT OK"
                check_value=2
                break
        print(char)
        for c in range(k,len(list_dict)):
            list_dict[c]=list_dict[c+1]

        del list_dict[len(list_dict)]
        i-=1
        j-=1
        k-=1
        print("YES")
        errordetected()
    print(list_dict)
    

def generate_frames():
    cap=cv2.VideoCapture('vid1.mp4')
    global flag,i
    while True :
        success,frame=cap.read()
        if not success:
            break
        if flag==1:
            i+=1
            list_dict[i]=[0,0,0,0,0,0,0]
            detection(frame)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

def generate_frames1():
    cap=cv2.VideoCapture('vid2.mp4')
    global flag,j
    while True :
        success,frame=cap.read()
        if not success:
            break
        if flag==2:
            if j+1 in list_dict:
                j+=1
                detection(frame)

        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


def generate_frames2():
    cap=cv2.VideoCapture('vid3.mp4')
    global flag,k
    while True :
        success,frame=cap.read()
        if not success:
            break
        if flag==3:
            if k+1 in list_dict:
                k+=1
                detection(frame)
        ret,buffer=cv2.imencode('.jpg',frame)
        frame=buffer.tobytes()
        yield(b'--frame\r\n'b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/video')
def video():
    return Response(generate_frames(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video1')
def video1():
    return Response(generate_frames1(),mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/video2')
def video2():
    return Response(generate_frames2(),mimetype='multipart/x-mixed-replace; boundary=frame')


@app.route('/change_flag')
def change_flag():
    global flag
    flag = 1
    return 'Flag has been changed to 1'

@app.route('/change_flag1')
def change_flag1():
    global flag
    flag = 2
    return 'Flag has been changed to 2'

@app.route('/change_flag2')
def change_flag2():
    global flag
    flag = 3
    return 'Flag has been changed to 3'

@app.route('/errordetected')
def errordetected():
    print("Values are transferring..")
    global check_value
    print(check_value)
    temp=check_value
    now=datetime.datetime.now()
    date_value=now.strftime("%Y-%m-%d")
    time_value=now.strftime("%H:%M:%S")
    hours=int(now.strftime("%H"))
    if(hours>=8 and hours<16):
        shift_value=1
    elif(hours>=16 and hours<24):
        shift_value=2
    else :
        shift_value=3

    id_value="XYZ0001"
    if temp==0:
        result_value="NA"
    elif temp==1:
        result_value="OK"
    else :
        result_value="NOT OK"
    # print(date_value,time_value,shift_value,id_value,result_value)
    save_db.insert(date_value,time_value,shift_value,id_value,result_value)
    print(temp)
    return {'value':temp}

@app.route('/reset')
def reset():
    global check_value
    check_value=0
    return index()


if __name__=="__main__":
    app.run(debug=True)