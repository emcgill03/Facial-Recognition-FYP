''''
Real Time Face Recogition
    ==> Each face stored on dataset/ dir, should have a unique numeric integer ID as 1, 2, 3, etc                       
    ==> LBPH computed model (trained beans) should be on trainer/ dir
Based on original code by Anirban Kar: https://github.com/thecodacus/Face-Recognition    

Developed by Marcelo Rovai - MJRoBot.org @ 21Feb18  
Modified by Eamon McGill for the detection of an object - in this case, a can of beans

'''

import cv2
import numpy as np
import os 

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/share/rpi-code/FacialRecognitionProject/trainer/trainer.yml')
# Bean cascade created with 'Cascade Trainer GUI' 
cascadePath = "/home/pi/share/rpi-code/FacialRecognitionProject/Object_Dataset/Beans dataset/classifier/beans_cascade.xml" 
beanCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Beans'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0, cv2.CAP_V4L)
cam.set(3, 960) # set video widht
cam.set(4, 720) # set video height

# Define min window size to be recognized as a face
minW = .25*cam.get(3)
minH = .25*cam.get(4)

while True:

    ret, img = cam.read()
    # img = cv2.flip(img, -1) # Flip vertically

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    beans = beanCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        # minSize = (int(minW), int(minH)),
        minSize = (200, 20)
       )
    
    for(x,y,w,h) in beans:  

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 75):
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,0,0), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (0,0,255), 2)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n [INFO] Exiting Program and cleanup stuff")
cam.release()
cv2.destroyAllWindows()
