import websocket
import threading
import time
from base64 import b64encode as enc
import json
import math
import requests

apikey = 'b2a1a39c-5a1c-4fcd-83f4-64e5a68cf2f9'.encode('ascii')

device_1 = '5dd3d92bc567e3296d8b179a'

blynk_auth = 'ZPbgCab2ZVSZi-M54vroCC-d8mjf0Jf2'

def hsv2rgb(h, s, v):
    h = float(h)
    s = float(s)
    v = float(v)
    h60 = h / 60.0
    h60f = math.floor(h60)
    hi = int(h60f) % 6
    f = h60 - h60f
    p = v * (1 - s)
    q = v * (1 - f * s)
    t = v * (1 - (1 - f) * s)
    r, g, b = 0, 0, 0
    if hi == 0: r, g, b = v, t, p
    elif hi == 1: r, g, b = q, v, p
    elif hi == 2: r, g, b = p, v, t
    elif hi == 3: r, g, b = p, q, v
    elif hi == 4: r, g, b = t, p, v
    elif hi == 5: r, g, b = v, p, q
    r, g, b = int(r * 255), int(g * 255), int(b * 255)
    return (r, g, b)

def changePwrState(state):
    url = 'http://188.166.206.43/' + str(blynk_auth) + '/update/v0'

    querystring = {"value":state}

    headers = {
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Host': "blynk-cloud.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def changeBrighness(bright):
    url = 'http://188.166.206.43/' + str(blynk_auth) + '/update/v5'

    querystring = {"value":bright}

    headers = {
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Host': "blynk-cloud.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def writeColor(r ,g ,b):
    url = 'http://188.166.206.43/' + str(blynk_auth) + '/update/v1'

    querystring = {"value":[r,g,b]}

    headers = {
        'User-Agent': "PostmanRuntime/7.18.0",
        'Accept': "*/*",
        'Cache-Control': "no-cache",
        'Postman-Token': "d001f97e-0181-4e40-8518-56d8890142ec,256ed8fa-93bb-4a16-ad34-96929283b2b0",
        'Host': "blynk-cloud.com",
        'Accept-Encoding': "gzip, deflate",
        'Connection': "keep-alive",
        'cache-control': "no-cache"
        }

    response = requests.request("GET", url, headers=headers, params=querystring)

    print(response.text)

def onSetPowerState(deviceId, value):
    if(deviceId == device_1):
        if(value == 'ON'):
            changePwrState(1)
        else:
            changePwrState(0)
        

def onSetColor(deviceId, value):
    if(deviceId == device_1):
        r ,g ,b = hsv2rgb(value['hue'] , value['saturation'] , value['brightness'])
        print(r ,g ,b)
        writeColor(r ,g ,b)


    # {'hue': 240, 'saturation': 1, 'brightness': 1}

def onSetBrightness(deviceId, value):
    if(deviceId == device_1):
        changeBrighness(value)

def selectionAction(deviceId, action, value):
    if action == 'setPowerState':
        onSetPowerState(deviceId, value)
    elif action == 'SetColor':
        onSetColor(deviceId, value)
    elif action == 'SetBrightness':
        onSetBrightness(deviceId, value)
    elif action == 'test':
        print('Received a test command')

def on_message(ws, message):  # Callback function on successfull response from server
    obj = json.loads(message)
    deviceId = obj['deviceId']
    action = obj['action']
    value = obj['value']
    selectionAction(deviceId, action, value)
    # print(message)      #Prints the JSON response 

def on_error(ws, error):
    print(error)

def on_close(ws):
    print('### closed ###')
    time.sleep(2)
    initiate()

def on_open(ws):
    print('### Initiating new websocket connection ###')

def initiate():
    websocket.enableTrace(True)

    ws = websocket.WebSocketApp('ws://iot.sinric.com',
                                header={
                                    'Authorization:' + enc(b'apikey: ' + apikey).decode('ascii')},
                                on_message=on_message,
                                on_error=on_error,
                                on_close=on_close)
    ws.on_open = on_open

    ws.run_forever()


if __name__ == '__main__':
    initiate()
