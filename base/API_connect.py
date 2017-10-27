from xero.auth import PrivateCredentials
from base.xero_reports_config import XeroReportsDef
from base.xero_parser import XeroParser
import time

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
    try:
        trial_balance_date = input("Please insert date for returning Trial Balance report (e.g. 2014-10-31): ")
    except ValueError:
        print("Date format has to be '%Y-%m-%d', e.g. 2014-10-31")

    xml_xero_reports = XeroReportsDef(authenticate)

    xml_contact_ids = xml_xero_reports.contact_ids()
    contact_ids = XeroParser(xml_contact_ids)
    contact_ids_list = contact_ids.list_of_contact_ids()

    xml_trial_balance = xml_xero_reports.trial_balance_as_at_date(trial_balance_date)
    trial_balance = XeroParser(xml_trial_balance, trial_balance_date)
    csv_trial_balance = trial_balance.trial_balance_to_csv()

    """
    aged_payables_header = XeroParser()
    csv_header_aged_payables = aged_payables_header.aged_payables_byContact_header()
    
    for contact in contact_ids_list:
        print(contact)
        try:
            xml_aged_payables = xml_xero_reports.aged_payables_from_to_date('2017-03-01','2017-03-31', contact)
            aged_payables = XeroParser(xml_aged_payables)
            csv_aged_payables = aged_payables.aged_payables_byContact_to_csv()
        except:
            time.sleep(5)
            xml_aged_payables = xml_xero_reports.aged_payables_from_to_date('2017-03-01', '2017-03-31', contact)
            aged_payables = XeroParser(xml_aged_payables)
            csv_aged_payables = aged_payables.aged_payables_byContact_to_csv()

    xml_profit_loss = xml_xero_reports.profit_loss_from_to_date('2017-03-01', '2017-07-31')
    profit_and_loss = XeroParser(xml_profit_loss)
    csv_profit_and_loss = profit_and_loss.profit_and_loss_to_csv()
    
    xml_aged_payables = xml_xero_reports.aged_payables_from_to_date('2017-06-01', '2017-06-30', '56c5b4e5-c9a4-4b17-8823-5411bb668766')
    aged_payables = XeroParser(xml_aged_payables)
    csv_aged_payables = aged_payables.aged_payables_byContact_to_csv()

    print(xml_aged_payables)
    #print(xml_contact_ids)
    #print(xml_profit_loss)
    """