'''
Haar Cascade Face, Smile and Eye detection with OpenCV  

Developed by Marcelo Rovai - MJRoBot.org @ 22Feb2018
Modified by Eamon McGill to add more cascades including body and glasses
'''

import numpy as np
import cv2

font = cv2.FONT_HERSHEY_SIMPLEX

# multiple cascades: https://github.com/Itseez/opencv/tree/master/data/haarcascades
faceCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml')
eyeCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_eye_tree_eyeglasses.xml')
smileCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_smile.xml')
upperCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_upperbody.xml')
bodyCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/haarcascade_fullbody.xml')
glassesCascade = cv2.CascadeClassifier('/home/pi/opencv/data/haarcascades/Glasses-detection-master/glasses_cascade.xml')

cap = cv2.VideoCapture(0)
cap.set(3,960) # set Width
cap.set(4,720) # set Height

while True:
    ret, img = cap.read()
   # img = cv2.flip(img, -1)
    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(
        gray,
        scaleFactor=1.3,
        minNeighbors=5,      
        minSize=(100, 20)
        )
        
    # Detection of a persons upper body     
    upperBody = upperCascade.detectMultiScale(
        gray,
        scaleFactor= 1.1,
        minNeighbors=8,
        minSize=(50, 100),
        )
        
    for (x,y,w,h) in upperBody:
        cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,40),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        id = "Upper Body"
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (0, 255, 40), 2)

    # Detection of a persons full body 
    fullBody = bodyCascade.detectMultiScale(
        gray,
        scaleFactor= 1.5,
        minNeighbors=5,
        minSize=(70, 70),
        )
        
    for (x,y,w,h) in fullBody:
        cv2.rectangle(img,(x,y),(x+w,y+h),(150,255,40),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w]
        id = "full Body"
        cv2.putText(img, str(id), (x,y), font, 1, (150, 255, 40), 2)
        
    # Detection of a face    
    for (x,y,w,h) in faces:
        cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
        roi_gray = gray[y:y+h, x:x+w]
        roi_color = img[y:y+h, x:x+w] 
 

        # Detection of eyes within a face 
        eyes = eyeCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors=5,
            minSize=(5, 5),
            )
        
        for (ex, ey, ew, eh) in eyes:
            cv2.rectangle(roi_color, (ex, ey), (ex + ew, ey + eh), (50, 255, 50), 2)

        # Detection of a smile within a face 
        smile = smileCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.2,
            minNeighbors=25,
            minSize=(20, 25),
            )
        
        for (xx, yy, ww, hh) in smile:
            cv2.rectangle(roi_color, (xx, yy), (xx + ww, yy + hh), (0, 255, 255), 2)
            id = "Smile"
            cv2.putText(img, "Smiling", (x+5,y-5), font, 1, (0, 255, 255), 2, cv2.LINE_AA )
        
        # Glasses detection (Not overly accurate)
        glasses = glassesCascade.detectMultiScale(
            roi_gray,
            scaleFactor= 1.5,
            minNeighbors= 6,
            minSize=(15,15),
            )
        for(gx,gy,gw,gh) in glasses:
            cv2.rectangle(roi_color, (gx,gy),(gx+gw, gy+gh), (255,255,0), 2)
            cv2.putText(roi_color,'glasses',(gx,gy-3), font, 0.5, (255,255,0), 2, cv2.LINE_AA)
            
                  
    cv2.imshow('video', img)
    

    k = cv2.waitKey(30) & 0xff
    if k == 27: # press 'ESC' to quit
        break

cap.release()
cv2.destroyAllWindows()
