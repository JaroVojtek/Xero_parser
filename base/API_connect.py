from xero.auth import PrivateCredentials
from base.xero_reports_config import XeroReportsDef

class XeroConnect():

    def __init__(self):
        self.consumer_key = 'MZ5BV2CY28XCI3JHHA7ADUFHOGKVMM'
        self.private_key_file = 'privatekey.pem'

    def return_private_key(self):
        with open(self.private_key_file) as keyfile:
            rsa_key = keyfile.read()
        return rsa_key

    def connect_to_xero(self):
        authenticate = PrivateCredentials(self.consumer_key, self.return_private_key())
        return authenticate

if __name__ == "__main__":
    connector = XeroConnect()
    authenticate = connector.connect_to_xero()

    xero_reports = XeroReportsDef(authenticate)
    trial_balance = xero_reports.trial_balance_as_at_date('2017-07-31')
    profit_loss = xero_reports.profit_loss_from_to_date('2017-07-01', '2017-07-31')
    aged_payables = xero_reports.aged_payables_from_to_date('2017-07-01', '2017-07-31') #it is by contact need to define

    print(profit_loss)