#  Copyright (c) 2020. Brendan Johnson. All Rights Reserved.

import requests
from datetime import datetime
import json
import urllib3
import time
from SmartCheck.__version__ import __version__,__smartcheck_api__
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
class Connection:
    def __init__(self, config):
        self._config = config
        self._token = None
        self._session = None
        self._loginObject = None
        self._retries = 0
        self._MAX_RETRIES = 12
    def _buildheaders(self):
        if self._token:
            return {    'Authorization': "Bearer " +self._token,
                        'X-Api-Version': __smartcheck_api__,
                        'Content-Type': 'application/json',
                        'User-Agent': 'smartcheck-sdk-mini ' + __version__
                        }
        else:
            return {    'X-Api-Version': __smartcheck_api__,
                        'Content-Type': 'application/json',
                        'User-Agent': 'smartcheck-sdk-mini ' + __version__
                        }
    def _setupSession(self):
        if self._session is None:
            self._retries = 0  # Only reset count the first time.
            self._session = requests.Session()
            if self._token is None:
                self._session.headers.update(self._buildheaders())
                self._GetToken()
            else:
               expires = datetime.strptime(self._loginObject['expires'], "%Y-%m-%dT%H:%M:%SZ")
               if datetime.utcnow() >= expires:
                    self._renewToken()
        return

    def get(self, url, params=None):
        self._setupSession()
        resp = self._session.get(self._config.host + url, verify=self._config.verify_ssl, params=params)
        if resp.status_code == 200:
            return json.loads(resp.content.decode('utf-8'))
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.get(url=url, params=params)
        return resp

    def delete(self, url, params=None):
        self._setupSession()
        resp = self._session.delete(self._config.host + url, verify=self._config.verify_ssl, params=params)
        if resp.status_code == 200:
            return "Success"
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.delete(url=url, params=params)
        return resp

    def post(self, url, data, params=None):
        self._setupSession()
        resp = self._session.post(self._config.host + url, verify=self._config.verify_ssl, json=data, params=params)
        if resp.status_code == 200:
            return "Success"
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.post(url=url, params=params)
        return resp

    def put(self, url, data,  params=None):
        self._setupSession()
        resp = self._session.put(self._config.host + url, verify=self._config.verify_ssl, json=data, params=params)
        if resp.status_code == 200:
            return "Success"
        elif resp.status_code == 429 and self._retries < self._MAX_RETRIES:
            self._retries += 1
            exp_backoff = (2**(self._retries+3))/1000
            time.sleep(exp_backoff)
            self.put(url=url, params=params)
        return resp


    def _renewToken(self):
        rtv = self._session.post(self._config.host + "/sessions/"+self._loginObject['id'], verify=self._config.verify_ssl)
        if rtv.status_code == 400:
            raise Exception(rtv.text)
        if rtv.status_code == 401:
            raise Exception("Unauthorized: Check your username/password.")
        if rtv.status_code == 200 or rtv.status_code == 201:
            self._loginObject = json.loads(rtv.text)
            self._token = self._loginObject['token']
            self._session.headers.update(self._buildheaders())
        return

    def _GetToken(self):
        loginObject = {
            "user": {
                "userID": self._config.username,
                "password": self._config.password
            }
        }
        rtv = self._session.post(self._config.host  + "/sessions", verify=self._config.verify_ssl, json=loginObject)
        if rtv.status_code == 400:
            raise Exception(rtv.text)
        if rtv.status_code == 401:
            raise Exception("Unauthorized: Check your username/password.")
        if rtv.status_code == 200 or rtv.status_code == 201:
            self._loginObject = json.loads(rtv.text)
            self._token = self._loginObject['token']
            self._session.headers.update(self._buildheaders())
        return