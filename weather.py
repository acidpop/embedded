#-*- encoding:UTF-8 -*-
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
while True:
    try:
        lcd.clear()
        lcd.message(cWeather1)
        sleep(2.5)
        lcd.clear()
        lcd.message(cWeather2)
        sleep(2.5)
    except KeyboardInterrupt:
        lcd.clear()
        exit(-1)
        
