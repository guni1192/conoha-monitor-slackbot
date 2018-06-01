import requests
import json
import datetime
import os


class ConoHaHandler:

    IDENTITY_URL = 'https://identity.tyo1.conoha.io/v2.0'
    COMPUTE_URL = 'https://compute.tyo1.conoha.io/v2'
    ACCOUNT_URL = 'https://account.tyo1.conoha.io/v1'

    def __init__(self, username, password, tenant_id):
        self.username = username
        self.password = password
        self.tenant_id = tenant_id

        self.base_header = {'Accept': 'application/json'}
        self.token = self.request_token()

    def request_token(self):
        url = self.IDENTITY_URL + '/tokens'
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
        url = self.COMPUTE_URL + str(self.tenant_id) + '/servers'

        header = self.base_header
        header['X-Auth-Token'] = self.token

        res = requests.get(url, headers=header)

        if (res.status_code == 200):
            return res.json()
        return res.status_code

    def get_vms_detail(self):
        url = self.COMPUTE_URL + '/' + str(self.tenant_id) + '/servers/detail'

        header = self.base_header
        header['X-Auth-Token'] = self.token

        res = requests.get(url, headers=header)

        if (res.status_code == 200):
            return res.json()
        return res.status_code

    def billing_invoices(self, limit=1000):

        url = self.ACCOUNT_URL + '/' + \
            str(self.tenant_id) + '/billing-invoices'

        params = {'limit': limit}

        header = self.base_header
        header['X-Auth-Token'] = self.token

        res = requests.get(url, headers=header, params=params)

        if (res.status_code == 200):
            return res.json()['billing_invoices']

        return res.status_code


def main():
    username = os.environ['CONOHA_USERNAME']
    password = os.environ['CONOHA_PASSWORD']
    tenant_id = os.environ['CONOHA_TENANT_ID']

    conoha = ConoHaHandler(username, password, tenant_id)
    # print(json.dumps(conoha.get_vms_detail()))

    for billing_invoice in conoha.billing_invoices(3):
        print(billing_invoice['due_date'] + ': ' +
              str(billing_invoice['bill_plus_tax']) + ' JPY')


if __name__ == '__main__':
    main(main)
