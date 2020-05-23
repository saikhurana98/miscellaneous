from sinric import SinricPro
from sinric import SinricProUdp
from credentials import (
    appKey,
    secretKey,
    deviceIdArr,
    blynkIdArr,
    pwrPinArr,
    rgbPinArr,
    slidePinArr,
    thermpPinArr,
)
from time import sleep
import requests


def onPowerState(did, state):
    # Alexa, turn ON/OFF Device
    index = deviceIdArr.index(did)
    changePwrState(blynkIdArr[index], pwrPinArr[index], state)
    print(f'Device ID: {did} \nStatue: {state}')
    return True, state


def onSetBrightness(did, state):
    # Alexa set device brightness to 40%
    # print(did, 'BrightnessLevel : ', state)
    return True, state


def onAdjustBrightness(did, state):
    # Alexa increase/decrease device brightness by 44
    index = deviceIdArr.index(did)
    changeBrighness(blynkIdArr[index], slidePinArr[index], state)
    return True, state


def onSetColor(did, r, g, b):
    # Alexa set device color to Red/Green
    index = deviceIdArr.index(did)
    writeColor(blynkIdArr[index], rgbPinArr[index], [r, g, b])
    return True


def onSetColorTemperature(did, value):
    index = deviceIdArr.index(did)
    writeColor(blynkIdArr[index], rgbPinArr[index], [255, 255, 255])
    return True


def onIncreaseColorTemperature(deviceId, value):
    return True, value


def onDecreaseColorTemperature(deviceId, value):
    return True, value


def onTargetTemperature(deviceId, value):
    print(f"Device-ID: {deviceId} \n Value: {value} \n")
    index = deviceIdArr.index(deviceId)
    setTemp(blynkIdArr[index], thermpPinArr[index], value)
    return True, value


def Events():
    # client.event_handler.raiseEvent(switchId, 'setPowerState',data={'state': 'On'})
    pass


event_callback = {"Events": Events}

callbacks = {
    "powerState": onPowerState,
    "setBrightness": onSetBrightness,
    "adjustBrightness": onAdjustBrightness,
    "setColor": onSetColor,
    "setColorTemperature": onSetColorTemperature,
    "increaseColorTemperature": onIncreaseColorTemperature,
    "decreaseColorTemperature": onDecreaseColorTemperature,
    "targetTemperature": onTargetTemperature,
}


def changePwrState(blynk_auth, pin, state):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"

    if state == "On":
        state = 1
    else:
        state = 0
    # print(state)
    querystring = {"value": state}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def changeBrighness(blynk_auth, pin, state):
    url = f"http://188.166.206.43/{blynkIdArr}/update/{pin}"

    querystring = {"value": state}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def writeColor(blynk_auth, pin, rgb):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"
    querystring = {"value": rgb}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Postman-Token": "d001f97e-0181-4e40-8518-56d8890142ec,256ed8fa-93bb-4a16-ad34-96929283b2b0",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


def setTemp(blynk_auth, pin, temp):
    url = f"http://188.166.206.43/{blynk_auth}/update/{pin}"

    querystring = {"value": temp}

    headers = {
        "User-Agent": "PostmanRuntime/7.18.0",
        "Accept": "*/*",
        "Cache-Control": "no-cache",
        "Postman-Token": "d001f97e-0181-4e40-8518-56d8890142ec,256ed8fa-93bb-4a16-ad34-96929283b2b0",
        "Host": "blynk-cloud.com",
        "Accept-Encoding": "gzip, deflate",
        "Connection": "keep-alive",
        "cache-control": "no-cache",
    }

    response = requests.request(
        "GET", url, headers=headers, params=querystring)


if __name__ == "__main__":
    client = SinricPro(
        appKey,
        deviceIdArr,
        callbacks,
        event_callbacks=event_callback,
        enable_log=True,
        restore_states=False,
        secretKey=secretKey,
    )
    # Set it to True to start logging request Offline Request/Response
    udp_client = SinricProUdp(callbacks, deviceIdArr, enable_trace=False)
    client.handle_all(udp_client)
