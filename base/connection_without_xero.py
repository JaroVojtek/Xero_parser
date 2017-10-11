from xero.auth import PrivateCredentials
import requests

with open('privatekey.pem') as keyfile:
    rsa_key = keyfile.read()


creds = PrivateCredentials("MZ5BV2CY28XCI3JHHA7ADUFHOGKVMM", rsa_key)

daterange = {'fromDate': '2017-09-01', 'toDate': '2017-09-30'}
response = requests.get(url='https://api.xero.com/api.xro/2.0/Reports/BankSummary', auth=creds.oauth, params=daterange)
print(response.text)