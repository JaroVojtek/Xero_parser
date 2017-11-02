import csv
import xml.etree.ElementTree as ET

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

        """
        root = self.parse_xml()
        report_name = "Masedi Electric Serve - Aged_Receivables_by_Contact"
        aged_receivables_csv = open(report_name + ".csv", 'a')
        writer = csv.writer(aged_receivables_csv, lineterminator='\n')

        contact_name = root[4][0][3][1].text

        row_number = []
        for child in root[4][0][6]:
            row_number.append(child.tag)
        try:
            sumary_first_number = float(root[4][0][6][len(row_number)-1][1][0][1][4][0].text)
            sumary_second_number = float(root[4][0][6][len(row_number)-1][1][0][1][5][0].text)
            sumarry_aged_payables = round(sumary_first_number-sumary_second_number,2)
            #closing_balance = float(root[4][0][6][len(row_number)-1][1][0][1][7][0].text)
            writer.writerow([contact_name, sumarry_aged_payables])
            #writer.writerow([contact_name,sumary_first_number])
            #writer.writerow([contact_name,closing_balance])
        except:
            #writer.writerow([contact_name,0.00])
            pass
        aged_receivables_csv.close()
        """

    def account_transactions(self, fromDate, filtered_bank_transactions):

        report_name = "Masedi Electric Serve - Account_Transactions_"+self.toDate
        account_transactions_csv = open(report_name + ".csv", 'w')
        writer = csv.writer(account_transactions_csv, lineterminator='\n')

        writer.writerow([report_name])
        reporting_period = "For the period {0} to {1}".format(fromDate,self.toDate)
        writer.writerow([reporting_period])
        writer.writerow("\n")
        writer.writerow(["Date","Source","Description","Reference","Debit","Credit"])
        writer.writerow("\n")

        account_transactions_dict = {}

        for f in filtered_bank_transactions:
            if not f['BankAccount']['Name'] in account_transactions_dict:
                account_transactions_dict[f['BankAccount']['Name']] = []
            else:
                date_string = f['DateString']
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
                account_transactions_row=[date_string, source, description, reference,debit,credit]
                account_transactions_dict[f['BankAccount']['Name']].append(account_transactions_row)

        for a in account_transactions_dict["FNB Bank"]:
            print(a)

        account_transactions_csv.close()





