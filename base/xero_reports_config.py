import requests
from datetime import datetime

class XeroReportsDef():

    def __init__(self, authenticate):
        self.authenticate = authenticate

    def xero_get_request(self,api_url, date_range=None):
        content = requests.get(url=api_url, auth=self.authenticate.oauth, params=date_range)
        return content.text

    def trial_balance_as_at_date(self, as_date):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/TrialBalance'
        date_range = {'date': datetime.strptime(as_date,'%Y-%m-%d')}
        return self.xero_get_request(api_url, date_range)

    def profit_loss_from_to_date(self, fromDate, toDate):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss'
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url,date_range)

    def aged_payables_from_to_date(self,fromDate, toDate, contactID):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/AgedPayablesByContact?ContactID='+contactID
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url,date_range)

    def contact_ids(self):
        api_url = 'https://api.xero.com/api.xro/2.0/Contacts'
        contacts = requests.get(url=api_url, auth=self.authenticate.oauth)
        return contacts.text

    def aged_receivables_from_to_date(self, fromDate, toDate, contactID):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/AgedReceivablesByContact?ContactID='+contactID
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url, date_range)

    def get_invoices(self,contactID):
        api_url = "https://api.xero.com/api.xro/2.0/Invoices/"
        return self.xero_get_request(api_url)








