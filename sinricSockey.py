try:
    import time
    import json
    import math
    import threading
    from base64 import b64encode as enc

    import requests
    import websocket
except Exception as e:
    print("Some Libraries are Missing {}".format(e))


class SecretKey(object):

    def __init__(self, api_key='', device_1='', blynk_auth=''):
        self.api_key = api_key.encode('ascii')
        self.device_1 = device_1
        self.blynk_id = blynk_auth


class BusinessLogic(object):

    def __init__(self, secret):
        self.secret_key = secret

    def selectLogic(self, deviceId, action, value):

        if action == 'setPowerState':
            self.onSetPowerState(deviceId, value)
        elif action == 'SetColor':
            self.onSetColor(deviceId, value)
        elif action == 'SetBrightness':
            self.onSetBrightness(deviceId, value)
        elif action == 'test':
            pass

    def onSetPowerState(self, deviceId, value):

        if(deviceId == self.secret_key.device_1):
            if(value == 'ON'):
                on = RequestBlynk(host="188.166.206.43",
                                  secret=self.secret_key, pin='v0', value=1)
                on.makeRequest()
            else:
                off = RequestBlynk(host="188.166.206.43",
                                   secret=self.secret_key, pin='v0', value=0)
                off.makeRequest()

    def onSetColor(self, deviceId, value):
        if(deviceId == self.secret_key.device_1):
            r, g, b = HSVtoRGB.hsv2rgb(value['hue'],
                                       value['saturation'],
                                       value['brightness'])

            write_color = RequestBlynk(host="188.166.206.43",
                                       secret=self.secret_key,
                                       pin='v1',
                                       value=[r, g, b])
            write_color.makeRequest()

    def onSetBrightness(self, deviceId, value):
        if(deviceId == secret_key.device_1):
            write_bright = RequestBlynk(host="188.166.206.43",
                                        secret=self.secret_key,
                                        pin='v5',
                                        value=value)
            write_bright.makeRequest()


class RequestBlynk(object):

    def __init__(self, host, secret, pin, value):
        self.host = host
        self.secret = secret
        self.pin = pin
        # self.completeUrl = self.host + \
        #     str(self.secret.blynk_id) + '/update/{}'.format(self.pin)
        #Using F-String to format the format the string
        self.complete_url = f'http://{self.host}/{self.secret.blynk_id}/update/{self.pin}'
        self.querystring = {
            "value": value}

        self.header = {
            'User-Agent': "PostmanRuntime/7.18.0",
            'Accept': "*/*",
            'Host': "blynk-cloud.com",
            'Accept-Encoding': "gzip, deflate",
            'Connection': "keep-alive",
            'cache-control': "no-cache"
        }

    def makeRequest(self):
        """
        Makes the Request to Blynk Server
        """
        response = requests.request("GET",
                                    self.complete_url,
                                    headers=self.header, 
                                    params=self.querystring)
        print(f'Corresping Blynk Call: \n')
        print(f' Host: "{self.complete_url}" \n Query: {self.querystring} \n BlynkApp-Pin: {self.pin} \n Response-Code: {response.status_code}')
        print(f'\n ****************************************************************** \n')

class HSVtoRGB(object):
    def __init__(self):
        pass

    @staticmethod
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
        if hi == 0:
            r, g, b = v, t, p
        elif hi == 1:
            r, g, b = q, v, p
        elif hi == 2:
            r, g, b = p, v, t
        elif hi == 3:
            r, g, b = p, q, v
        elif hi == 4:
            r, g, b = t, p, v
        elif hi == 5:
            r, g, b = v, p, q
        r, g, b = int(r * 255), int(g * 255), int(b * 255)
        return (r, g, b)


class Sinric(object):

    def __init__(self, secret):
        self.secret = secret
        self._domainName = 'ws://iot.sinric.com'
        self._header = {'Authorization:' +
                        enc(b'apikey: ' + self.secret.api_key).decode('ascii')}
        self.businesslogic = BusinessLogic(secret)

    @property
    def start(self):
        websocket.enableTrace(True)
        self.ws = websocket.WebSocketApp(
            self._domainName,
            header=self._header,
            on_message=self.on_message,
            on_error=self.on_error,
            on_close=self.on_close
        )
        self.ws.on_open = self.on_open
        self.ws.run_forever()

    def on_message(self, message):  # Callback function on successfull response from server
        obj = json.loads(message)
        deviceId = obj['deviceId']
        action = obj['action']
        value = obj['value']
        print(f'\n ****************************************************************** \n')
        print(f'Data Recieved from Sinric: \n')
        print(f' Raw-json:{message} \n DeviceId: {deviceId} \n Action: {action} \n Value: {value} \n')
        self.businesslogic.selectLogic(deviceId, action, value)
        

    def on_open(self):
        print('### Initiating new websocket connection ###')

    def on_error(self, error):
        print(error)

    def on_close(self):
        print('### closed ###')
        time.sleep(2)
        self.start()


if __name__ == '__main__':

    secret_key = SecretKey(api_key='b2a1a39c-5a1c-4fcd-83f4-64e5a68cf2f9',
                           device_1='5dd3d92bc567e3296d8b179a',
                           blynk_auth='ZPbgCab2ZVSZi-M54vroCC-d8mjf0Jf2')
    sinric = Sinric(secret_key)
    sinric.start
