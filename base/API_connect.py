from xero_requests_config import XeroRequestsDef
from xero_parser import XeroParserGET, XeroParserPUT, put_contacts_xml
from xero import Xero
from xero.auth import PrivateCredentials
import calendar
import re
import time
from openpyxl import load_workbook
import datetime

class XeroConnect():

    def __init__(self):
        #self.consumer_key = 'MZ5BV2CY28XCI3JHHA7ADUFHOGKVMM' #Masendi company
        self.consumer_key = 'ZDG10NLLJ8LMVN4BKQ9L5TK6XZ6IBN' #TopApp
        self.private_key_file = 'privatekey.pem'

    def return_private_key(self):
        with open(self.private_key_file) as keyfile:
            rsa_key = keyfile.read()
        return rsa_key

    def connect_to_xero(self):
        authenticate = PrivateCredentials(self.consumer_key, self.return_private_key())
        return authenticate

if __name__ == "__main__":
    #Choose GET o POST options available in Xero script
    answer = 0
    while answer==0:
        option = input("Please choose if you want to proceed with get or posts actions."
                       " Type: [GET/POST] and press Enter: ").lower()
        if option=="get" or option=="post":
            answer = 1

    #Create authentification token
    connector = XeroConnect()
    authenticate = connector.connect_to_xero()
    xero = Xero(authenticate)
    xero_requests = XeroRequestsDef(authenticate)

    if option == "get":
        try:
            reporting_month = input("Please insert number of month for which you want to generate reports (eg. '4'):  ")
            if len(reporting_month) == 1:
                reporting_month = "0"+reporting_month
            reporting_year = int(input("Please insert year: "))
            last_day_in_month = calendar.monthrange(reporting_year, int(reporting_month))
            fromDate = str(reporting_year) + "-" + reporting_month + "-01"
            toDate = str(reporting_year) + "-" + reporting_month + "-" + str(last_day_in_month[1])
        except ValueError:
            print("You have to insert numbers between 1-12, please try again")

        raw_string = 'Date >= DateTime({0}, {1}, 1) && Date < DateTime({0}, {1}, {2})'.format(str(reporting_year), reporting_month, str(last_day_in_month[1]))
        #raw_string = 'Date >= DateTime({0}, 1, 1) && Date < DateTime({0}, 10, 31)'.format(str(current_year),
        #                                                                                     reporting_month,
        #                                                                                      str(last_day_in_month[1]))
        filtered_invoices = xero.invoices.filter(raw=raw_string)
        #filtered_invoices = xero.invoices.filter(Contact_ContactID='4923a86c-478a-4905-810f-864092a469ea',raw=raw_string)

        filtered_bank_transactions = xero.banktransactions.filter(raw=raw_string)
        filtered_payments = xero.payments.filter(raw=raw_string)

        #filtered_bank_transfers = xero.banktransfers.filter(raw=raw_string)

        report_gen = XeroParserGET(toDate=toDate)
        report_gen.aged_receivables_to_csv(filtered_invoices)
        report_gen.aged_payables_to_csv(filtered_invoices)
        report_gen.expences_by_contact_to_csv(filtered_invoices)
        report_gen.income_by_contact_to_csv(filtered_invoices)
        report_gen.account_transactions(fromDate, filtered_bank_transactions,filtered_payments)

        xml_invoices = xero_requests.get_invoices()
        #report_gen.invoices_csv_troubleshoot(xml_invoices)

        #with open('all_invoices_xml','w') as f:
        #    f.write(xml_invoices)
        #report_gen.list_of_contact_ids(xml_contact_ids)

        xml_credit_notes = xero_requests.get_credit_notes()
        #print(xml_credit_notes)
        report_gen.credit_notes_troubleshoot_append(xml_credit_notes)

        xml_contact_ids = xero_requests.contact_ids()
        with open('contact_ids.txt', 'w') as f:
            f.write(xml_contact_ids)
        #report_gen.balances_troubleshoot_append(xml_contact_ids)

        xml_trial_balance = xero_requests.trial_balance_as_at_date(toDate)
        report_gen.trial_balance_to_csv(xml_trial_balance)

        xml_balance_sheet = xero_requests.balance_sheet_as_at_date(toDate)
        #print(xml_balance_sheet)

        xml_profit_loss = xero_requests.profit_loss_from_to_date(fromDate, toDate)
        report_gen.profit_and_loss_to_csv(xml_profit_loss)

    else:
        #-----------------PUT INVOICES API------------------------------------
        """
        file_name = input("Please provide a csv file name, containing data to upload: ")
        workbook = load_workbook(file_name, data_only=True)
        sheet = workbook.active
        rows = sheet.rows
        offset = 1
        contact_id_list = xero.contacts.all()

        for i, row in enumerate(rows):
            if i < offset:
                continue
            invoices_list = [cell.value for cell in row]

            put_type= "ACCPAY"

            for contact in contact_id_list:
                if contact['Name']==invoices_list[0]:
                    put_contact_id = contact['ContactID']
                    print(put_contact_id)
            put_date=invoices_list[1]
            put_invoice_number=invoices_list[2]
            put_reference = invoices_list[3]
            put_description = invoices_list[4]
            put_unit_amount = invoices_list[5]
            put_tax_amount = invoices_list[6]

            put_gen = XeroParserPUT(put_type, put_contact_id, put_date, put_invoice_number,
                                    put_reference, put_description,
                                    put_unit_amount, put_tax_amount)

            invoices_xml = put_gen.put_invoices_xml()
            xml_put_invoices = xero_requests.put_invoices(invoices_xml)
            print(xml_put_invoices.status_code)
            print(xml_put_invoices.text)
            time.sleep(2)
            #break
        """
        #---------------------------Contacts Importing---------------------------
        with open('unimported_contacts.txt', 'r') as f:
            xml_contact = f.read()
        list_of_contacts = put_contacts_xml(xml_contact)
        for c in list_of_contacts:
            time.sleep(3)
            company_name = re.search('<Name>(.*)</Name>',c)
            xml_put_contacts = xero_requests.put_contacts(c)
            print(company_name.group(1)+": "+str(xml_put_contacts.status_code))
        #------------------------------------------------------------------------


