from xero.auth import PrivateCredentials
from base.xero_reports_config import XeroReportsDef
from base.xero_parser import XeroParser
from xero import Xero
import calendar
import datetime

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
        current_year = current.year
        last_day_in_month = calendar.monthrange(current_year, int(reporting_month))
        fromDate = str(current_year)+"-"+reporting_month+"-01"
        toDate = str(current_year)+"-"+reporting_month+"-"+str(last_day_in_month[1])
    except ValueError:
        print("You have to insert numbers between 1-12, please try again")

    connector = XeroConnect()
    authenticate = connector.connect_to_xero()

    xero = Xero(authenticate)

    raw_string = 'Date >= DateTime({0}, {1}, 1) && Date < DateTime({0}, {1}, {2})'.format(str(current_year),reporting_month, str(last_day_in_month[1]))
    filtered_invoices = xero.invoices.filter(raw=raw_string)
    #filtered_invoices = xero.invoices.filter(Contact_ContactID='d8831e4f-3f06-4a39-b230-54182a942e9f',raw=raw_string)

    filtered_bank_transactions = xero.banktransactions.filter(raw=raw_string)

    filtered_bank_transfers = xero.banktransfers.filter(raw=raw_string)
    #for b in filtered_bank_transfers:
    #    print(b)

    filtered_payments = xero.payments.filter(raw=raw_string)
    #for b in filtered_payments:
    #    print(b)

    report_gen = XeroParser(toDate=toDate)
    report_gen.aged_receivables_to_csv(filtered_invoices)
    report_gen.aged_payables_to_csv(filtered_invoices)
    report_gen.expences_by_contact_to_csv(filtered_invoices)
    report_gen.income_by_contact_to_csv(filtered_invoices)
    report_gen.account_transactions(fromDate, filtered_bank_transactions)

    xml_xero_reports = XeroReportsDef(authenticate)

    xml_contact_ids = xml_xero_reports.contact_ids()
    report_gen.list_of_contact_ids(xml_contact_ids)

    xml_trial_balance = xml_xero_reports.trial_balance_as_at_date(toDate)
    report_gen.trial_balance_to_csv(xml_trial_balance)

    xml_profit_loss = xml_xero_reports.profit_loss_from_to_date(fromDate, toDate)
    report_gen.profit_and_loss_to_csv(xml_profit_loss)

    """

    for contact in contact_ids_list:
        try:
            time.sleep(1)
            invoice = xero.invoices.filter(Contact_ContactID=contact, raw='Date >= DateTime(2017, 03, 01) && Date < DateTime(2017, 06, 30)')
        except:
            time.sleep(5)
            invoice = xero.invoices.filter(Contact_ContactID=contact,
                                           raw='Date >= DateTime(2017, 06, 01) && Date < DateTime(2017, 06, 30)')
        try:
            time.sleep(1)
            cont = xero.contacts.get(contact)
        except:
            time.sleep(5)
            cont = xero.contacts.get(contact)
        together = 0
        for i in invoice:
            together += float((i['AmountDue']))
        print(cont[0]['Name']+","+str(together))


    #print(xero.invoices.filter(ContactID='56c5b4e5-c9a4-4b17-8823-5411bb668766,18138aa1-0390-4f2a-a9ef-98addb6e2a2',raw='Date >= DateTime(2017, 06, 01) && Date < DateTime(2017, 06, 30)'))

    aged_payables_header = XeroParser()
    csv_header_aged_payables = aged_payables_header.aged_payables_byContact_header()

    for contact in contact_ids_list:
        print(contact)
        try:
            xml_aged_payables = xml_xero_reports.aged_payables_from_to_date('2017-06-01','2017-06-30', contact)
            aged_payables = XeroParser(xml_aged_payables)
            csv_aged_payables = aged_payables.aged_payables_byContact_to_csv()

            xml_aged_receivables = xml_xero_reports.aged_receivables_from_to_date('2017-06-01', '2017-06-30', contact)
            aged_receivables = XeroParser(xml_aged_receivables)
            csv_aged_receivables = aged_receivables.aged_receivables_byContact_to_csv()
        except:
            time.sleep(5)
            xml_aged_payables = xml_xero_reports.aged_payables_from_to_date('2017-06-01', '2017-06-30', contact)
            aged_payables = XeroParser(xml_aged_payables)
            csv_aged_payables = aged_payables.aged_payables_byContact_to_csv()

            xml_aged_receivables = xml_xero_reports.aged_receivables_from_to_date('2017-06-01', '2017-06-30', contact)
            aged_receivables = XeroParser(xml_aged_receivables)
            csv_aged_receivables = aged_receivables.aged_receivables_byContact_to_csv()
    """



