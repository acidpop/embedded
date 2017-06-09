#_*_coding: utf-8 _*_
#!/usr/bin/env python
# Requires PyAudio and PySpeech.

import sys
reload(sys)
sys.setdefaultencoding('utf-8')

#speech recognition
import speech_recognition as sr
from time import ctime
import time
import os
from gtts import gTTS

#lcd
import json
import requests
from Adafruit_CharLCD import Adafruit_CharLCD
from time import sleep

params = {"version": "1", "city":"부산", "county":"부산진구","village":"가야1동"}
headers = {"appKey": "0b7e8caa-3d84-3f65-89b5-eb05b4b31070"}
r = requests.get("http://apis.skplanetx.com/weather/current/hourly", params=params, headers=headers)

data = r.json()

weather = data["weather"]["hourly"]
cTime = weather[0]["timeRelease"]
cSky = weather[0]["sky"]["name"]
cWind = weather[0]["wind"]["wspd"]
cTemp = weather[0]["temperature"]["tc"]

cWeather1 = "      Time\n"+cTime
cWeather2 = "      Temp\n    " + cTemp +"'C"
lcd = Adafruit_CharLCD(rs=22, en=11, d4=23, d5=10, d6=9, d7=25, cols=16, lines=2)

def viewLCD():
    """Play the label"""
    lcd.clear()
    lcd.message(cWeather1)
    sleep(2.5)
    lcd.clear()
    lcd.message(cWeather2)
    sleep(2.5)

def speak(audioString):
    print(audioString)
    tts = gTTS(text=audioString, lang='ko')
    tts.save("audio1.mp3")
    os.system("omxplayer -o local audio1.mp3")
 
def recordAudio():
    # Record Audio
    r = sr.Recognizer()
    r.energy_threshold = 500
    
    with sr.Microphone(device_index = 1, sample_rate = 44100) as source:
        #print("Say something!")
        #audio = r.listen(source)
        r.adjust_for_ambient_noise(source)
        print("Say something!")
        audio = r.listen(source)
        print("Done listening!")
    # Speech recognition using Google Speech Recognition
    data = ""
    try:
        # Uses the default API key
        # To use another API key: `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
        data = r.recognize_google(audio, language = "ko-KR")
        print("You said: " + data)
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
 
    return data
 
def jarvis(data):
    if "날씨" in data:
        weatherInfo = "오늘의 온도는 "+ cTemp+"도이고  날씨는" + cSky + "입니다."
        viewLCD()
        speak(weatherInfo)
        viewLCD()
        lcd.clear()
        
    if "시간" in data:
        speak("현재 시간은 "+ctime()+"년 입니다.")
 
    if "안녕" in data:
        speak("안녕하세요 주인님")
 
# initialization
time.sleep(2)
while 1:
    data = recordAudio()
    jarvis(data)
