import csv
import xml.etree.ElementTree as ET

class XeroParser():

    def __init__(self,xml_content, date_range=None):
        self.xml_content = xml_content
        self.date_range = date_range

    def parse_xml(self):
        root = ET.fromstring(self.xml_content)
        return root

    def list_of_contact_ids(self):
        root = self.parse_xml()
        contactIDs = []
        for child in root[4].iter('ContactID'):
            contactIDs.append(child.text)
        return contactIDs

    def trial_balance_to_csv(self):
        root = self.parse_xml()
        report_name = "Masedi Electric Serve - Trial Balance_"+self.date_range
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

    def aged_payables_byContact_to_csv(self):
        root = self.parse_xml()
        report_name = "Masedi Electric Serve - Aged_Payables_by_Contact"
        aged_payables_csv = open(report_name+".csv", 'w')
        writer = csv.writer(aged_payables_csv, lineterminator='\n')

        writer.writerow([report_name])
        #for child in root[4][0][6][2][1][2][1][7]:
        #    value_at_month = child.text

        aged_payables_csv.close()



