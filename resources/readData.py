import json
import time
import Adafruit_BBIO.GPIO as GPIO
import Adafruit_BBIO.ADC as ADC

GPIO.setup("P9_11", GPIO.IN)
GPIO.setup("P9_12", GPIO.IN)
ADC.setup()

data = {'Uptime': 0,
        'Button1': 0,
        'Button2': 0,
        'Temperature C': 0,
        'Temperature F': 0}

while(True):
        temp = ADC.read_raw("P9_40") / 22.75
        data['Temperature C'] = temp
        temp = temp *9 /5
        temp = temp + 32
        data['Temperature F'] = temp
        data['Uptime'] += 1
        data['Button1'] = GPIO.input("P9_11")
        data['Button2'] = GPIO.input("P9_12")

        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        time.sleep(1)
