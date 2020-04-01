# Script will listen for the command 'Weather'.
# When detected it will ask the user what city they want the forecast for
# If a face is recognised, a greeting message will play 

import speech_recognition as sr
import os
import time
import re
import requests
import pprint
import cv2
import numpy as np

from gtts import gTTS

# Weather Setup
r = sr.Recognizer()
m = sr.Microphone()

no_help = False
is_weather = False

with m as source: r.adjust_for_ambient_noise(source)

API_key = "018e225be83c72f71f5cbd274b7010d4"
base_url = "http://api.openweathermap.org/data/2.5/weather?"
kelvin = 273.15

# Facial Recognition Setup
recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('/home/pi/share/rpi-code/FacialRecognitionProject/trainer/trainer.yml')
cascadePath = "/home/pi/opencv/data/haarcascades/haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath);

font = cv2.FONT_HERSHEY_SIMPLEX

#iniciate id counter
id = 0

# names related to ids: example ==> Marcelo: id=1,  etc
names = ['None', 'Eamon'] 

# Initialize and start realtime video capture
cam = cv2.VideoCapture(0, cv2.CAP_V4L)
cam.set(3, 960) # set video widht
cam.set(4, 720) # set video height

# Define min window size to be recognized as a face
minW = .25*cam.get(3)
minH = .25*cam.get(4)

intro = False
c = 10
d = 5

def askWeather():
    
    os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/help.mp3")
    
    try:
        # Recognise speech using Google Speech Recognition
        os.system('cls' if os.name == 'nt' else 'clear')
        with m as source: audio = r.listen(source)
        value = r.recognize_google(audio)
        
        no_help = bool(re.search('no', value, re.IGNORECASE))
        is_weather = bool(re.search('weather', value, re.IGNORECASE))
        
        if no_help is True:
        
            os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/no_help.mp3")
        
        elif is_weather is True:
        
            os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/sure.mp3")
            
            with m as source: audio = r.listen(source)
            city_name = r.recognize_google(audio)
            
            final_url = base_url + "q=" + city_name + "&APPID=" + API_key
            
            weather_data = requests.get(final_url).json()
            # pprint.pprint(weather_data)
            
            valid = weather_data['cod']
            
            if valid == 200:
                temp = weather_data['main']['temp']
                temp = temp - kelvin
                temp = str(round(temp,2))
                
                wind_speed = weather_data['wind']['speed']
                description = weather_data['weather'][0]['description']

                tts = gTTS('It currently looks like {} in {}. The temperature is {} degrees celcius, with a windspeed of {} meters per second.'.format(description, city_name, temp, wind_speed), lang='en')
                tts.save('weather.mp3')
                os.system("mplayer -ao alsa -noconsolecontrols weather.mp3")
                
            else:
                os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/no_city.mp3")
        else:
            os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/not_weather.mp3")
    
    except sr.UnknownValueError:
        os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/no_idea.mp3")
    
    except sr.RequestError as e:
        os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/no_google.mp3")
        
while True:

    os.system('cls' if os.name == 'nt' else 'clear')

    ret, img = cam.read()

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)

    faces = faceCascade.detectMultiScale( 
        gray,
        scaleFactor = 1.2,
        minNeighbors = 5,
        # minSize = (int(minW), int(minH)),
        minSize = (200, 20)
       )

    for(x,y,w,h) in faces:

        cv2.rectangle(img, (x,y), (x+w,y+h), (0,255,0), 2)

        id, confidence = recognizer.predict(gray[y:y+h,x:x+w])

        # Check if confidence is less them 100 ==> "0" is perfect match 
        if (confidence < 75): # Confidence level could be lowered if more training data and power was available
            id_num = id
            id = names[id]
            confidence = "  {0}%".format(round(100 - confidence))
            
            if intro is False:
                os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/hello_Eamon.mp3") #Greeting when it recognises my face
                intro = True
                c = 0
                askWeather()
                
            else:           
                if c > 29:
                    if id_num == 1:
                        os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/return.mp3")
                        c = 0
                        askWeather()
                c += 1
        else:
            id = "unknown"
            confidence = "  {0}%".format(round(100 - confidence))
            
            if d > 4:
                os.system("mplayer -ao alsa -noconsolecontrols /home/pi/share/unknown.mp3")
                d = 0            
            
            d += 1
        
        cv2.putText(img, str(id), (x+5,y-5), font, 1, (255,0,0), 2)
        cv2.putText(img, str(confidence), (x+5,y+h-5), font, 1, (0,0,255), 2)  
    
    cv2.imshow('camera',img) 

    k = cv2.waitKey(10) & 0xff # Press 'ESC' for exiting video
    if k == 27:
        break

# Do a bit of cleanup
print("\n[INFO] Exiting program and cleaning up stuff!\n")
cam.release()
cv2.destroyAllWindows()
