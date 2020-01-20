'''
Panasonic session, using Panasonic Comfort Cloud app api
'''

from datetime import datetime
import json
import requests
import os
import urllib3

from . import urls
from . import constants

def _validate_response(response):
    """ Verify that response is OK """
    if 2 == response.status_code // 100:
        return
    raise ResponseError(response.status_code, response.text)

class Error(Exception):
    ''' Panasonic session error '''
    pass

class RequestError(Error):
    ''' Wrapped requests.exceptions.RequestException '''
    pass

class LoginError(Error):
    ''' Login failed '''
    pass

class ResponseError(Error):
    ''' Unexcpected response '''
    def __init__(self, status_code, text):
        super(ResponseError, self).__init__(
            'Invalid response'
            ', status code: {0} - Data: {1}'.format(
                status_code,
                text))
        self.status_code = status_code
        self.text = json.loads(text)

class Session(object):
    """ Verisure app session

    Args:
        username (str): Username used to login to verisure app
        password (str): Password used to login to verisure app

    """

    def __init__(self, username, password, tokenFileName='~/.panasonic-token', raw=False, verifySsl=True):
        self._username = username
        self._password = password
        self._session = requests.Session()
        self._groups = None
        self._devices = None
        self._deviceIndexer = {}
        self._raw = raw

        if verifySsl == False:
            urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            self._verifySsl = verifySsl
        else:
            self._verifySsl = os.path.join(os.path.dirname(__file__),
                    "certificatechain.pem")

    def __enter__(self):
        self.login()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.logout()

    def login(self):
        """ Login to eolia app api """

        response = None

        payload = {
            "idpw":{
                "id": self._username,
                "next_easy":True,
                "pass": self._password,
                "terminal_type":3
            }
        }

        if self._raw: print("--- creating token by authenticating")

        try:
            response = self._session.post(urls.login(), json=payload, headers=self._headers(), verify=self._verifySsl)
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise LoginError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

    def logout(self):
        """ Logout """

    def _headers(self):
        now = datetime.now()
        return {
            "Accept": "application/json",
            "Content-Type": "application/json;charset=UTF-8",
            "X-Eolia-Date": now.strftime("%Y-%m-%dT%H:%M:%S")
        }

    def get_devices(self):
        self._devices = []

        response = None

        if self._raw: print("--- getting device list")

        try:
            response = self._session.get(urls.get_devices(), headers=self._headers(), verify=self._verifySsl)
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise Error(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---\n")

        devices = json.loads(response.text)['ac_list']

        for device in devices:
            self._devices.append({
                "id": device["appliance_id"],
                "name": device["nickname"],
                "model": device["product_code"]
            })

        return self._devices

    def dump(self, id):

        response = None

        try:
            response = self._session.get(urls.status(id), headers=self._headers(), verify=self._verifySsl)

            if response.status_code != 200:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)
        return json.loads(response.text)

    # def history(self, id, mode, date, tz="+01:00"):
    #     deviceGuid = self._deviceIndexer.get(id)

    #     if(deviceGuid):
    #         response = None

    #         try:
    #             dataMode = constants.dataMode[mode].value
    #         except KeyError:
    #             raise Exception("Wrong mode parameter")

    #         payload = {
    #             "deviceGuid": deviceGuid,
    #             "dataMode": dataMode,
    #             "date": date,
    #             "osTimezone": tz
    #         }

    #         try:
    #             response = requests.post(urls.history(), json=payload, headers=self._headers(), verify=self._verifySsl)

    #             if 2 != response.status_code // 100:
    #                 raise ResponseError(response.status_code, response.text)

    #         except requests.exceptions.RequestException as ex:
    #             raise RequestError(ex)

    #         _validate_response(response)

    #         if(self._raw is True):
    #             print("--- history()")
    #             print("--- raw beginning ---")
    #             print(response.text)
    #             print("--- raw ending    ---")

    #         _json = json.loads(response.text)
    #         return {
    #             'id': id,
    #             'parameters': self._read_parameters(_json)
    #         }

    #     return None

    def get_device(self, id):

        response = None

        try:
            response = self._session.get(urls.status(id), headers=self._headers(), verify=self._verifySsl)

            if response.status_code != 200:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- get_device()")
            print("--- raw beginning ---")
            print(response.text)
            print("--- raw ending    ---")


        _json = json.loads(response.text)
        return {
            'id': id,
            'parameters': self._read_parameters(_json)
        }

    def set_device(self, id, **kwargs):
        """ Set parameters of device

        Args:
            id  (str): Id of the device
            kwargs   : {temperature=float}, {mode=OperationMode}, {fanSpeed=FanSpeed}, {power=Power}, {airSwingVertical=}
        """

        payload = {}

        if kwargs is not None:
            for key, value in kwargs.items():
                if key == 'power' and isinstance(value, constants.Power):
                    payload['operation_status'] = value.value

                if key == 'temperature':
                    payload['temperature'] = value

                if key == 'mode' and isinstance(value, constants.OperationMode):
                    payload['operation_mode'] = value.value

                if key == 'fanSpeed' and isinstance(value, constants.FanSpeed):
                    payload['wind_volume'] = value.value

                if key == 'airSwingVertical' and isinstance(value, constants.AirSwingUD):
                    payload['wind_direction'] = value.value
        
        # Set misc other parameters in the payload
        payload['airquality'] = False # Get 400 error if this is true, not sure what it does
        payload['nanoex'] = True
        payload['silence_control'] = False
        payload['timer_value'] = 0
        # payload['operation_token'] = 'xxxxxxxxxxxxxxxx' # Not sure what this is, it doesn't seem like it's required

        response = None

        if(self._raw is True):
            print("--- set_device()")
            print("--- raw out beginning ---")
            print(payload)
            print("--- raw out ending    ---")

        try:
            response = self._session.put(urls.status(id), json=payload, headers=self._headers(), verify=self._verifySsl)

            print(response.status_code)
            if 2 != response.status_code // 100:
                raise ResponseError(response.status_code, response.text)

        except requests.exceptions.RequestException as ex:
            raise RequestError(ex)

        _validate_response(response)

        if(self._raw is True):
            print("--- raw in beginning ---")
            print(response.text)
            print("--- raw in ending    ---\n")

        _json = json.loads(response.text)

        return True

    def _read_parameters(self, parameters = {}):
        value = {}

        _convert = {
                'inside_temp': 'temperatureInside',
                'outside_temp': 'temperatureOutside',
                'temperature': 'temperature',
            }
        for key in _convert:
            if key in parameters:
                value[_convert[key]] = parameters[key]

        if 'operation_status' in parameters:
            value['power'] = constants.Power(parameters['operation_status'])

        if 'operation_mode' in parameters:
            value['mode'] = constants.OperationMode(parameters['operation_mode'])

        if 'wind_volume' in parameters:
            value['fanSpeed'] = constants.FanSpeed(parameters['wind_volume'])

        if 'wind_direction' in parameters:
            value['airSwingVertical'] = constants.AirSwingUD(parameters['wind_direction'])

        return value
