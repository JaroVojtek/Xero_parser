from xero.auth import PrivateCredentials
from xero import Xero

with open("privatekey.pem") as keyfile:
    rsa_key = keyfile.read()

credentials = PrivateCredentials("MZ5BV2CY28XCI3JHHA7ADUFHOGKVMM", rsa_key)

xero = Xero(credentials)

reports = xero.reports.get(u'BankSummary')
print(reports)




