from xero_reports_config import XeroReportsDef
from xero_parser import XeroParser
from xero import Xero
from xero.auth import PrivateCredentials
import calendar
import datetime
import json



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
    try:
        reporting_month = input("Please insert number of month for which you want to generate reports (eg. '4'):  ")
        if len(reporting_month) == 1:
            reporting_month = "0"+reporting_month
        current = datetime.datetime.now()
        #current_year = current.year
        current_year = int(input("Please insert year: "))
        last_day_in_month = calendar.monthrange(current_year, int(reporting_month))
        fromDate = str(current_year)+"-"+reporting_month+"-01"
        toDate = str(current_year)+"-"+reporting_month+"-"+str(last_day_in_month[1])
    except ValueError:
        print("You have to insert numbers between 1-12, please try again")

    connector = XeroConnect()
    authenticate = connector.connect_to_xero()

    xero = Xero(authenticate)

    raw_string = 'Date >= DateTime({0}, {1}, 1) && Date < DateTime({0}, {1}, {2})'.format(str(current_year),reporting_month, str(last_day_in_month[1]))
    #raw_string = 'Date >= DateTime({0}, 1, 1) && Date < DateTime({0}, 10, 31)'.format(str(current_year),
    #                                                                                     reporting_month,
    #                                                                                      str(last_day_in_month[1]))
    filtered_invoices = xero.invoices.filter(raw=raw_string)
    #filtered_invoices = xero.invoices.filter(Contact_ContactID='4923a86c-478a-4905-810f-864092a469ea',raw=raw_string)

    filtered_bank_transactions = xero.banktransactions.filter(raw=raw_string)
    filtered_payments = xero.payments.filter(raw=raw_string)

    #filtered_bank_transfers = xero.banktransfers.filter(raw=raw_string)

    """
    file = open("all_invoices_1-10_2017", 'w')

    for b in filtered_invoices:
        file.write(json.dumps(b, indent=4, sort_keys=True, default=str))

    file.close()
    """
    report_gen = XeroParser(toDate=toDate)
    report_gen.aged_receivables_to_csv(filtered_invoices)
    report_gen.aged_payables_to_csv(filtered_invoices)
    report_gen.expences_by_contact_to_csv(filtered_invoices)
    report_gen.income_by_contact_to_csv(filtered_invoices)
    report_gen.account_transactions(fromDate, filtered_bank_transactions,filtered_payments)

    xml_xero_reports = XeroReportsDef(authenticate)

    xml_invoices = xml_xero_reports.get_invoices('75f5f830-41ad-47f6-9685-f5044b885106')
    #print(xml_invoices)
    report_gen.invoices_csv_troubleshoot(xml_invoices)
    #with open('all_invoices_xml','w') as f:
    #    f.write(xml_invoices)
    #report_gen.list_of_contact_ids(xml_contact_ids)

    xml_credit_notes = xml_xero_reports.get_credit_notes()
    #print(xml_credit_notes)
    report_gen.credit_notes_troubleshoot_append(xml_credit_notes)

    xml_contact_ids = xml_xero_reports.contact_ids()
    #print(xml_contact_ids)
    #report_gen.balances_troubleshoot_append(xml_contact_ids)

    xml_trial_balance = xml_xero_reports.trial_balance_as_at_date(toDate)
    report_gen.trial_balance_to_csv(xml_trial_balance)

    xml_balance_sheet = xml_xero_reports.balance_sheet_as_at_date(toDate)
    #print(xml_balance_sheet)

    xml_profit_loss = xml_xero_reports.profit_loss_from_to_date(fromDate, toDate)
    report_gen.profit_and_loss_to_csv(xml_profit_loss)





