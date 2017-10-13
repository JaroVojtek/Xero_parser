import requests
from datetime import datetime

class XeroReportsDef():

    def __init__(self, authenticate):
        self.authenticate = authenticate

    def trial_balance_as_at_date(self, as_date):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/TrialBalance'
        date_param = datetime.strptime(as_date,'%Y-%m-%d')
        content = requests.get(url=api_url, auth=self.authenticate.oauth, params={'date': date_param})
        return content.text

    def profit_loss_from_to_date(self, fromDate, toDate):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss'
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        content = requests.get(url=api_url, auth=self.authenticate.oauth, params=date_range)
        return content.text

    def aged_payables_from_to_date(self, fromDate, toDate):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/AgedPayablesByContact'
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        content = requests.get(url=api_url, auth=self.authenticate.oauth, params=date_range)
        return content.text







