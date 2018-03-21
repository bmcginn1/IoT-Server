import json
import time
import datetime
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC
import netifaces as ni

GPIO.setup("P9_11", GPIO.IN)
GPIO.setup("P9_12", GPIO.IN)
ADC.setup()
startTime = datetime.datetime.now()
button1 = GPIO.input("P9_11")
button2 = GPIO.input("P9_12")
tempMin = 1000;
tempMax = 0;
data = {'Uptime': 0,
        'Button1': 0,
        'Button2': 0,
        'Temperature C': 0,
        'Temperature F': 0,
        'IP': 'n/a',
        'DateTime': 'n/a',
        'LastChange': '',
        'LastButton': '',
        'TempMin': 0,
        'TempMax': 0}

ni.ifaddresses('eth0')
data['IP'] = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

while(True):

        temp = ADC.read_raw("P9_40") / 22.75
        data['Temperature C'] = temp
        temp = temp *9 /5
        temp = temp + 32
        data['Temperature F'] = temp
        #if(data['Uptime'] % 36000 == 0): #When an hour has elapsed we re set the max/min temperatures
        #    tempMax = 0
        #    tempMin = 1000
        if(temp > tempMax):
            tempMax = temp
            data['TempMax'] = temp
        if(temp < tempMin):
            tempMin = temp
            data['TempMin'] = temp
        timeNow = datetime.datetime.now()
        data['DateTime'] = timeNow.isoformat()
        data['Uptime'] = str(timeNow - startTime)


        if(button1 != GPIO.input("P9_11")):
            data['Button1'] = GPIO.input("P9_11")
            data['LastButton'] = 'Button1/P9_11'
            data['LastChange'] = data['DateTime']

        if(button2 != GPIO.input("P9_12")):
            data['Button2'] = GPIO.input("P9_12")
            data['LastButton'] = 'Button2/P9_12'
            data['LastChange'] = data['DateTime']

#        data['Button1'] = GPIO.input("P9_11")
#        data['Button2'] = GPIO.input("P9_12")

        with open('/var/www/html/resources/data.json', 'w') as outfile:
            json.dump(data, outfile)

        time.sleep(.5)
