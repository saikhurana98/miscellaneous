import requests
import time
from datetime import datetime

url = "http://10.1.0.100:8090/login.xml"
username = "auni12345"
password = "Welcome1"
update_interval = 1800

def login():
    payload = "mode=191&username=" + str(username) + "&password=" + str(password) + "&a=1565939518046&producttype=0"
    headers = {
        'Connection': "keep-alive",
        'Content-Length': "82",
        'Content-Type': "application/x-www-form-urlencoded",
        'Cache-Control': "no-cache",
        'Host': "10.1.0.100:8090"
        }

    response = requests.request("POST", url, data=payload, headers=headers)

    print(response)
    return(response)

def main():
    login()
    start = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
    while True:
        time.sleep(1)
        end = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
        diff = end - start
        if (diff.seconds >= update_interval):
            login()
            start = datetime.strptime(str(datetime.now()),"%Y-%m-%d %H:%M:%S.%f")
        

if __name__ == "__main__":
    main()
