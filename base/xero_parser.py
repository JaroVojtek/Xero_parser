import csv
import xml.etree.ElementTree as ET
from datetime import datetime

class XeroParser():

    def __init__(self, toDate=None):
        self.toDate = toDate

    def parse_xml(self,  xml_content):
        root = ET.fromstring(xml_content)
        return root

    def list_of_contact_ids(self, xml_content):
        root = self.parse_xml(xml_content)
        contactIDs = []
        for child in root[4].iter('ContactID'):
            contactIDs.append(child.text)
        return contactIDs

    def invoices_csv_troubleshoot(self, xml_content):
        root = self.parse_xml(xml_content)
        report_name = "Masedi Electric Serve - All invoices"
        all_invoices_csv = open(report_name+'.csv', 'w')
        writer = csv.writer(all_invoices_csv, lineterminator = '\n', delimiter ='|')

        writer.writerow([report_name])
        writer.writerow("\n")
        writer.writerow(['Contact ID','Contact Name', 'Invoice Number', 'Reference', 'Date', 'Status',
                         'Type', 'SubTotal', 'TotalTax', 'Total', 'Amount Due', 'Amount Credited',
                         'AmountPaid'])

        invoices = len(root.findall(".//Invoice"))
        for invoice in range(invoices):
            contact_id, contact_name, invoice_date, subtotal, totaltax, total = ["" for i in range(6)]
            payment_type, status, amount_paid, amount_credited, amount_due = ["" for i in range(5)]
            invoice_number, reference = ["" for i in range(2)]
            for child in root[4][invoice].iter():
                    if child.tag == 'ContactID':
                        contact_id = child.text
                    elif child.tag == 'Name':
                        contact_name = child.text
                    elif child.tag == 'Date':
                        timestamp = datetime.strptime(child.text, '%Y-%m-%dT%H:%M:%S')
                        if datetime(2017, 1, 1) < timestamp < datetime(2017, 10, 31):
                            invoice_date = child.text
                        else:
                            continue
                    elif child.tag == 'SubTotal':
                        subtotal = child.text
                    elif child.tag == 'TotalTax':
                        totaltax = child.text
                    elif child.tag == 'Total':
                        total = child.text
                    elif child.tag == 'Type':
                        payment_type = child.text
                    elif child.tag == 'Status':
                        status = child.text
                    elif child.tag == 'AmountDue':
                        amount_due = child.text
                    elif child.tag == 'AmountCredited':
                        amount_credited = child.text
                    elif child.tag == 'AmountPaid':
                        amount_paid = child.text
                    elif child.tag == 'InvoiceNumber':
                        invoice_number = child.text
                    elif child.tag == 'Reference':
                        reference = child.text

            writer.writerow([contact_id, contact_name, invoice_number, reference, invoice_date, status,
                             payment_type, subtotal, totaltax, total, amount_due, amount_credited, amount_paid])

        all_invoices_csv.close()

    def credit_notes_troubleshoot_append(self, xml_content):
        root = self.parse_xml(xml_content)
        report_name = "Masedi Electric Serve - All invoices"
        all_invoices_csv = open(report_name + '.csv', 'a')
        writer = csv.writer(all_invoices_csv, lineterminator='\n', delimiter='|')

        credit_notes = len(root.findall(".//CreditNote"))
        for credit_note in range(credit_notes):
            contact_id, contact_name, invoice_date, subtotal, totaltax, total, payment_type = ["" for i in range(7)]
            status, invoice_number, reference = ["" for i in range(3)]
            for child in root[4][credit_note].iter():
                if child.tag == 'ContactID':
                    contact_id = child.text
                elif child.tag == 'Name':
                    contact_name = child.text
                elif child.tag == 'Date':
                    timestamp = datetime.strptime(child.text, '%Y-%m-%dT%H:%M:%S')
                    if datetime(2017, 1, 1) < timestamp < datetime(2017, 10, 31):
                        invoice_date = child.text
                    else:
                        continue
                elif child.tag == 'SubTotal':
                    subtotal = child.text
                elif child.tag == 'TotalTax':
                    totaltax = child.text
                elif child.tag == 'Total':
                    total = child.text
                elif child.tag == 'Type':
                    payment_type = child.text
                elif child.tag == 'Status':
                    status = child.text
                elif child.tag == 'InvoiceNumber':
                    invoice_number = child.text
                elif child.tag == 'Reference':
                    reference = child.text

            writer.writerow([contact_id, contact_name, invoice_number, reference, invoice_date, status,
                             payment_type, subtotal, totaltax, total])

        all_invoices_csv.close()

    def balances_troubleshoot_append(self, xml_content):
        root = self.parse_xml(xml_content)
        report_name = "Masedi Electric Serve - All invoices"
        all_invoices_csv = open(report_name + '.csv', 'a')
        writer = csv.writer(all_invoices_csv, lineterminator='\n', delimiter='|')

        balances = len(root.findall(".//Contact"))
        for balance in range(balances):
            for child in root[4][balance].iter():
                if child.tag == 'ContactID':
                    contact_id = child.text
                elif child.tag == 'Name':
                    contact_name = child.text
                elif child.tag == 'AccountsReceivable':
                    account_receivable_title = child.tag
                    account_receivable = child.find('Outstanding').text
                elif child.tag == 'AccountsPayable':
                    account_payable_title = child.tag
                    account_payable = child.find('Outstanding').text

            writer.writerow([contact_id, contact_name, '2017-01-01T00:00:00', 'Balance',
                             account_receivable_title, account_receivable,
                             account_payable_title, account_payable])

        all_invoices_csv.close()

    def trial_balance_to_csv(self, xml_content):
        root = self.parse_xml(xml_content)
        report_name = "Masedi Electric Serve - Trial Balance_"+self.toDate
        trial_balance_csv = open(report_name+".csv", 'w')
        writer = csv.writer(trial_balance_csv, lineterminator='\n')

        writer.writerow([report_name])
        trial_balance_header = []
        for child in root[4][0][6][0][1].iter('Value'):
            trial_balance_header.append(child.text)
        writer.writerow(trial_balance_header)

        for item in [1, 2, 3, 4, 5]:
            trial_balance_item_title = root[4][0][6][item][1].text
            writer.writerow("\n")
            writer.writerow([trial_balance_item_title])

            trial_balance_item_rows_number = len(root[4][0][6][item][2])
            for row in range(trial_balance_item_rows_number):
                trial_balance_item = []
                for child in root[4][0][6][item][2][row][1]:
                    if child[0].tag == 'Value':
                        try:
                            trial_balance_item.append(float(child[0].text))
                        except:
                            trial_balance_item.append("\""+child[0].text+"\"")
                    else:
                        trial_balance_item.append(0)
                writer.writerow(trial_balance_item)

        writer.writerow("\n")
        trial_balance_total = []
        for child in root[4][0][6][6][1][0][1].iter('Value'):
            trial_balance_total.append(child.text)
        writer.writerow(trial_balance_total)

        trial_balance_csv.close()

    def aged_payables_to_csv(self,filtered_invoices):

        aged_payables_dict = {}

        for f in filtered_invoices:
            if f['Type'] == "ACCPAY" and not f['Contact']['Name'] in aged_payables_dict:
                aged_payables_dict[f['Contact']['Name']] = f['AmountDue']
            elif f['Type'] == "ACCPAY" and f['Contact']['Name'] in aged_payables_dict:
                aged_payables_dict[f['Contact']['Name']] = round(aged_payables_dict[f['Contact']['Name']] +
                                                                 f['AmountDue'],2)

        report_name = "Masedi Electric Serve - Aged_Payables_"+self.toDate
        aged_payables_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(aged_payables_csv, lineterminator='\n')

        writer.writerow([report_name])
        writer.writerow(["",self.toDate])

        for key, value in aged_payables_dict.items():
            writer.writerow([key, value])

        aged_payables_csv.close()

    def expences_by_contact_to_csv(self, filtered_invoices):

        expences_dict = {}

        for f in filtered_invoices:
            if f['Type'] == "ACCPAY" and not f['Contact']['Name'] in expences_dict:
                expences_dict[f['Contact']['Name']] = f['SubTotal']
            elif f['Type'] == "ACCPAY" and f['Contact']['Name'] in expences_dict:
                expences_dict[f['Contact']['Name']] = round(expences_dict[f['Contact']['Name']] + f['SubTotal'],2)

        report_name = "Masedi Electric Serve - Expences by Contact_" + self.toDate
        expences_by_contact_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(expences_by_contact_csv, lineterminator='\n')

        writer.writerow([report_name])
        writer.writerow(["", self.toDate])

        for key, value in expences_dict.items():
            writer.writerow([key, value])

        expences_by_contact_csv.close()

    def income_by_contact_to_csv(self, filtered_invoices):

        income_dic = {}

        for f in filtered_invoices:
            if f['Type'] == "ACCREC" and not f['Contact']['Name'] in income_dic:
                income_dic[f['Contact']['Name']] = f['SubTotal']
            elif f['Type'] == "ACCREC" and f['Contact']['Name'] in income_dic:
                income_dic[f['Contact']['Name']] = round(income_dic[f['Contact']['Name']] + f['SubTotal'],2)

        report_name = "Masedi Electric Serve - Income by Contact_" + self.toDate
        income_by_contact_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(income_by_contact_csv, lineterminator='\n')

        writer.writerow([report_name])
        writer.writerow(["", self.toDate])

        for key, value in income_dic.items():
            writer.writerow([key, value])

        income_by_contact_csv.close()

    def profit_and_loss_to_csv(self, xml_content):
        root = self.parse_xml(xml_content)
        report_name = "Masedi Electric Serve - Profit  Loss_"+self.toDate
        profit_and_loss_csv = open(report_name+".csv","w")
        writer = csv.writer(profit_and_loss_csv, lineterminator="\n")

        writer.writerow([report_name])
        profit_and_loss_date_header = root[4][0][6][0][1][1][0].text
        writer.writerow("\n")
        writer.writerow(["",profit_and_loss_date_header])

        number_of_sections = len(root[4][0][6])

        for section in range(1, number_of_sections):
            if section == 3 or section == 6:
                writer.writerow("\n")
                profit_and_loss_item_rows_number = len(root[4][0][6][section][1])
                for row in range(profit_and_loss_item_rows_number):
                    profit_and_loss_item = []
                    for child in root[4][0][6][section][1][row][1]:
                        if child[0].tag == 'Value':
                            try:
                                profit_and_loss_item.append(float(child[0].text))
                            except:
                                profit_and_loss_item.append("\"" + child[0].text + "\"")
                        else:
                            profit_and_loss_item.append(0)
                    writer.writerow(profit_and_loss_item)
            else:
                profit_and_loss_section_header = root[4][0][6][section][1].text
                writer.writerow("\n")
                writer.writerow([profit_and_loss_section_header])

                profit_and_loss_item_rows_number = len(root[4][0][6][section][2])
                for row in range(profit_and_loss_item_rows_number):
                    profit_and_loss_item = []
                    for child in root[4][0][6][section][2][row][1]:
                        if child[0].tag == 'Value':
                            try:
                                profit_and_loss_item.append(float(child[0].text))
                            except:
                                profit_and_loss_item.append("\"" + child[0].text + "\"")
                        else:
                            profit_and_loss_item.append(0)
                    writer.writerow(profit_and_loss_item)

        profit_and_loss_csv.close()

    def aged_receivables_to_csv(self, filtered_invoices):

        aged_receivables_dict = {}

        for f in filtered_invoices:
            if f['Type'] == "ACCREC" and not f['Contact']['Name'] in aged_receivables_dict:
                aged_receivables_dict[f['Contact']['Name']] = f['AmountDue']
            elif f['Type'] == "ACCREC" and f['Contact']['Name'] in aged_receivables_dict:
                aged_receivables_dict[f['Contact']['Name']] = round(aged_receivables_dict[f['Contact']['Name']] + f['AmountDue'],2)

        report_name = "Masedi Electric Serve - Aged_Receivables_"+self.toDate
        aged_receivables_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(aged_receivables_csv, lineterminator='\n')

        writer.writerow([report_name])
        writer.writerow(["",self.toDate])

        for key, value in aged_receivables_dict.items():
            writer.writerow([key, value])

        aged_receivables_csv.close()

    def account_transactions(self, fromDate, filtered_bank_transactions, filtered_payments):

        report_name = "Masedi Electric Serve - Account_Transactions_"+self.toDate
        account_transactions_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(account_transactions_csv, lineterminator='\n')

        writer.writerow([report_name])
        reporting_period = "For the period {0} to {1}".format(fromDate,self.toDate)
        writer.writerow([reporting_period])
        writer.writerow("\n")
        writer.writerow(["Date","Source","Description","Reference","Debit","Credit"])
        writer.writerow("\n")

        account_ids_dict = {}

        for f in filtered_bank_transactions:
            if not f['BankAccount']['AccountID'] in account_ids_dict:
                account_ids_dict[f['BankAccount']['AccountID']] = f['BankAccount']['Name']

        account_transactions_dict = {}

        for f in filtered_bank_transactions:
            if not f['BankAccount']['Name'] in account_transactions_dict:
                account_transactions_dict[f['BankAccount']['Name']] = []

            date_string = f['Date']
            source = f['Type']
            try:
                description = f['Contact']['Name']
            except:
                description = ""
            try:
                reference = f['Reference']
            except:
                reference = ""
            if source == "RECEIVE" or source == "RECEIVE-TRANSFER":
                debit = f['Total']
                credit = 0
            else:
                debit = 0
                credit = f['Total']
            account_transactions_row = [date_string, source, description, reference, debit, credit]
            account_transactions_dict[f['BankAccount']['Name']].append(account_transactions_row)

        account_payments_dict = {}

        for f in filtered_payments:

            if not account_ids_dict[f['Account']['AccountID']] in account_payments_dict:
                account_payments_dict[account_ids_dict[f['Account']['AccountID']]] = []

            date_string = f['Date']
            source = f['PaymentType']
            try:
                description = "Payment: " + f['Invoice']['Contact']['Name']
            except:
                description = ""
            try:
                reference = f['Invoice']['InvoiceNumber']
            except:
                reference = ""
            if source == "ACCRECPAYMENT":
                debit = f['BankAmount']
                credit = 0
            else:
                debit = 0
                credit = f['BankAmount']
            account_payments_row = [date_string, source, description, reference, debit, credit]
            account_payments_dict[account_ids_dict[f['Account']['AccountID']]].append(account_payments_row)

        for bank_account in account_transactions_dict.keys():
            writer.writerow([bank_account])
            for transactions in account_transactions_dict[bank_account]:
                writer.writerow(transactions)
            try:
                for payments in account_payments_dict[bank_account]:
                    writer.writerow(payments)
            except:
                pass
            writer.writerow("\n")
        account_transactions_csv.close()





