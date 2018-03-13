import pandas as pd
from datetime import datetime
import csv
import re
import os
import sys

xlsx_name = input("Please xlsx file name (withouth .xlsx extention) to convert: ")
csv_name = xlsx_name + "_export.csv"

if os.path.isfile(csv_name):
    print("{0} file already exists, please remove it before running this script or move it to another directory".format(
        csv_name))
    sys.exit()

error_file = xlsx_name + "_error_list.txt"
csv_file_handler = open(csv_name, 'a')
writer = csv.writer(csv_file_handler, lineterminator="\n")

df = pd.read_excel(xlsx_name + '.xlsx', 'Table 1', index_col=None)
column_names = ['col_' + str(col) for col in range(len(df.columns))]
column_names[0] = 'Name'
df.columns = column_names


def write_invoices(contact, department_address, invoice_list):
    try:
        if 'Page' in invoice_list[1]:
            invoice_list = invoice_list[2:]

    except:
        pass

    if invoice_list:
        try:
            try:
                if '\n' in invoice_list[0]:
                    inv_date = invoice_list[0].split('\n')
                    inv_num = invoice_list[1].replace('\n', ' ').split(' ')
                    inv_net_amount = re.sub(' R', '\nR', invoice_list[2])
                    inv_net_amount = inv_net_amount.split('\n')
                    inv_vat_amount = re.sub(' R', '\nR', invoice_list[3])
                    inv_vat_amount = inv_vat_amount.split('\n')
                    inv_incl_amount = re.sub(' R', '\nR', invoice_list[4])
                    inv_incl_amount = inv_incl_amount.split('\n')
                    for num in range(len(inv_date)):
                        inv_list = []
                        inv_list.append(contact)
                        inv_list.append(department_address)
                        inv_list.append(inv_date[num])
                        inv_list.append(inv_num[num])
                        inv_list.append(inv_net_amount[num])
                        inv_list.append(inv_vat_amount[num])
                        inv_list.append(inv_incl_amount[num])
                    # print(inv_list)
                    # input()
                    writer.writerow(inv_list)
                else:
                    invoice_list.insert(0, contact)
                    invoice_list.insert(1, department_address)
                    # print(invoice_list)
                    # input()
                    writer.writerow(invoice_list)
            except:
                invoice_list.insert(0, contact)
                invoice_list.insert(1, department_address)
                writer.writerow(invoices_list)
                # print(invoice_list)
                # input()
        except:
            with open(error_file, 'a') as error_file:
                error_file.write(invoice_list)


row = df.iloc[:, 0].iteritems()
for index, value in row:
    if 'Date' in str(value):
        contact = df.iloc[index - 1, 0]
        temp_index = index
        temp_index += 1
        while 'Department:' not in str(df.iloc[temp_index, 0]):
            temp_index += 1
        if df.iloc[temp_index, 0] > 'Department:':
            department_address = ""
            department_row = df.iloc[temp_index, :].fillna("")
            for column in range(len(department_row)):
                department_address += str(department_row.iloc[column]) + "  "
                department_address = department_address.replace("\n", "**")
                department_address = department_address.replace("  ", "**")
                department_address_list = re.split("\*+", department_address)
            inv_num = int((len(department_address_list) - 3) / 5)
            for i in range(inv_num):
                department = department_address_list[1]
                invoice_date_num = department_address_list[2 + (i * 2):2 * (i + 1) + 2]
                invoice_values = department_address_list[2 + (2 * inv_num) + (i * 3):2 + (2 * inv_num) + 3 + (i * 3)]
                invoice_write = [contact, department] + invoice_date_num + invoice_values
                try:
                    is_date_infront = datetime.strptime(invoice_write[1], '%d-%b-%y')
                    if is_date_infront:
                        inv_date = invoice_write[1]
                        inv_department = invoice_write[2]
                        invoice_write[1] = inv_department
                        invoice_write[2] = inv_date
                except:
                    pass
                # print(invoice_write[0],invoice_write[1],invoice_write[2:])
                # input()
                write_invoices(invoice_write[0], invoice_write[1], invoice_write[2:])
        else:
            department_address = ""
            department_row = df.iloc[temp_index, 1:].fillna("")
            for column in range(len(department_row)):
                department_address += str(department_row.iloc[column])
            temp_index += 1
            invoices_list = []
            while 'Department Total' not in str(df.iloc[temp_index, 0]) and 'Site:' not in str(df.iloc[temp_index, 0]):
                invoices_list = []
                for col in range(len(df.columns)):
                    if not pd.isnull(df.iloc[temp_index, col]):
                        invoices_list.append(df.iloc[temp_index, col])
                # print(contact, department_address, invoices_list)
                # input()
                write_invoices(contact, department_address, invoices_list)
                temp_index += 1

            temp_index += 1
            while 'Supplier Total' not in str(df.iloc[temp_index, 0]) and 'Site:' not in str(df.iloc[temp_index, 0]):
                if 'Department:' in str(df.iloc[temp_index, 0]):
                    department_address = ""
                    department_row = df.iloc[temp_index, 1:].fillna("")
                    for column in range(len(department_row)):
                        department_address += str(department_row.iloc[column])
                    temp_index += 1
                    while 'Department Total' not in str(df.iloc[temp_index, 0]):
                        invoices_list = []
                        for col in range(len(df.columns)):
                            if not pd.isnull(df.iloc[temp_index, col]):
                                invoices_list.append(df.iloc[temp_index, col])
                        write_invoices(contact, department_address, invoices_list)
                        temp_index += 1
                temp_index += 1

csv_file_handler.close()

print("\nCSV export file was saved to {0} file".format(csv_name))
if os.path.isfile(error_file):
    print("During XLSX conversion some errors occured. You can find error list in {0} file".format(error_file))
else:
    print("NO errors occured during XLSX-CSV conversion")
print("\nScript Finished\nNOTE: If you want to rerun this conversion script for same file, Please remove alerady " +
      "existing {0} file.\nThank you.".format(csv_name))
