import requests
import json
import datetime
import os


class ConoHaHandler:
    def __init__(self, username, password, tenant_id):
        self.username = username
        self.password = password
        self.tenant_id = tenant_id

        self.identity_url = 'https://identity.tyo1.conoha.io/'
        self.compute_url = 'https://compute.tyo1.conoha.io/v2/'

        self.base_header = {'Accept': 'application/json'}
        self.token = self.request_token()

    def request_token(self):  # トークンの取得処理
        url = self.identity_url + '/v2.0/tokens'
        data = {
            'auth': {
                'tenantId': self.tenant_id,
                'passwordCredentials': {
                    'username': self.username,
                    'password': self.password,
                }
            }
        }
        res = requests.post(url, data=json.dumps(data),
                            headers=self.base_header)
        return res.json()['access']['token']['id']

    def get_vms(self):
        url = self.compute_url + str(self.tenant_id) + '/servers'

        header = self.base_header
        header['X-Auth-Token'] = self.token

        res = requests.get(url, headers=self.base_header)

        if (res.status_code == 200):
            return res.json()
        return res.status_code

    def get_vms_detail(self):
        url = self.compute_url + str(self.tenant_id) + '/servers/detail'

        header = self.base_header
        header['X-Auth-Token'] = self.token

        res = requests.get(url, headers=self.base_header)

        if (res.status_code == 200):
            return res.json()
        return res.status_code


def main():
    username = os.environ['CONOHA_USERNAME']
    password = os.environ['CONOHA_PASSWORD']
    tenant_id = os.environ['CONOHA_TENANT_ID']

    conoha = ConoHaHandler(username, password, tenant_id)
    print(json.dumps(conoha.get_vms_detail()))
