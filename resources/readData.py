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
history ={'Hours': 0}
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
        'TempMax': 0
        }

ni.ifaddresses('eth0')
data['IP'] = ni.ifaddresses('eth0')[ni.AF_INET][0]['addr']

while(True):

        timeNow = datetime.datetime.now()
        timePassed = timeNow - startTime
        data['DateTime'] = timeNow.isoformat()
        data['Uptime'] = str(timePassed)

        if(timePassed.seconds % 3600 == 0): #When an hour has elapsed we re set the max/min temperatures
            history['Hours']= timePassed.hours
            history[timePassed.seconds] = {'Min': ('%.2f' % tempMin), 'Max': ('%.2f' % tempMax)}
            with open('/var/www/html/resources/tempHistory.json', 'w') as houtfile:
                json.dump(history, houtfile)
            tempMax = 0
            tempMin = 1000

        temp = ADC.read_raw("P9_40") / 22.75
        data['Temperature C'] = '%.2f' % temp
        temp = temp *9 /5
        temp = temp + 32
        data['Temperature F'] = '%.2f' % temp

        if(temp > tempMax):
            tempMax = temp
            data['TempMax'] = '%.2f' % temp
        if(temp < tempMin):
            tempMin = temp
            data['TempMin'] = '%.2f' % temp

        button1State = GPIO.input("P9_11")
        button2State = GPIO.input("P9_12")

        if(button1 != button1State):
            button1 = button1State
            data['Button1'] = button1
            data['LastButton'] = 'Button1/P9_11'
            data['LastChange'] = data['DateTime']

        if(button2 != button2State):
            button2 = button2State
            data['Button2'] = button2
            data['LastButton'] = 'Button2/P9_12'
            data['LastChange'] = data['DateTime']

        with open('/var/www/html/resources/data.json', 'w') as outfile:
            json.dump(data, outfile)

        time.sleep(.1)
