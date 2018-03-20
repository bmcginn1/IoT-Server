import json
import time

data = {'Uptime': 0,
        'Button1': 0,
        'Button2': 0,
        'Temperature': 0}

while(True):
        data['Uptime'] += 1
        with open('data.json', 'w') as outfile:
            json.dump(data, outfile)
        time.sleep(1)
