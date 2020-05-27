#!/usr/bin/pyton3
'''
Documentation 
'''

import requests
from requests.exceptions import HTTPError


class Blynk:

    ''' Widget Class '''

    def __init__(self, server, auth, pin, raise_exceptions=False):
        self.server = server
        self.auth = auth
        self.pin = pin
        self.raise_exceptions = raise_exceptions

    def get_value(self):
        
        ''' Get the current state of the pin '''

        url = f'http://{self.server}/{self.auth}/get/{self.pin}'

        headers = {
            "Content-Type": "applciation/json",
        }

        try:
            response = requests.request("GET", url, headers=headers)
            if response.status_code == 200:
                return response.json()[0]
            return False
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False

    def get_project(self):

        ''' Returns project connected '''

        url = f'http://{self.server}/{self.auth}/project'

        headers = {
            "Content-Type": "applciation/json",
        }

        try:
            response = requests.request("GET", url, headers=headers)
            return response.json() if response.status_code == 200 else False
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False

    def write_value(self, value):

        ''' Write a value to a pin '''

        url = f"http://{self.server}/{self.auth}/update/{self.pin}"

        querystring = {"value": list(value)}

        headers = {
            "Content-Type": "applciation/json",
        }

        try:
            response = requests.request(
                "GET", url, headers=headers, params=querystring)
            return bool(response.status_code == 200)
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False

    @property
    def is_hardware_connected(self):

        ''' Return true if Hardware is Online else false '''

        url = f"http://{self.server}/{self.auth}/isHardwareConnected"

        try:
            response = requests.request(
                "GET", url)
            if response.status_code == 200:
                return bool(response.text.encode('utf8'))
            return False
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False

    @property
    def is_app_connected(self):

        ''' Return true if App is connected else false '''

        url = f"http://{self.server}/{self.auth}/isAppConnected"

        try:
            response = requests.request(
                "GET", url)
            if response.status_code == 200:
                return bool(response.text.encode('utf8') == "true")
            return False
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False

    def set_property(self, widget_property, value):

        ''' Set Property of a widget '''

        url = f"http://{self.server}/{self.auth}/update/{self.pin}"
        querystring = {widget_property: value}

        try:
            response = requests.request("GET", url, params=querystring)
            return response.text.encode('utf8')
        except HTTPError:
            if self.raise_exceptions:
                raise HTTPError
            return False
