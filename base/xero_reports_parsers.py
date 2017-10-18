import csv
import xml.etree.ElementTree as ET


def parse_xml(xml_content):
    root = ET.fromstring(xml_content)
    return root

def trial_balance_parser(xml_content):
    root = parse_xml(xml_content)
    trial_balance_csv = open('Masedi Electric Serve - Trial Balance.csv', 'w')
    writer = csv.writer(trial_balance_csv, lineterminator='\n')

    trial_balance_header = []
    for child in root[4][0][6][0][1].iter('Value'):
        trial_balance_header.append(child.text)
    writer.writerow(trial_balance_header)
    writer.writerow("\n")

    revenue_title = root[4][0][6][1][1].text
    writer.writerow([revenue_title])

    revenue_rows_number = len(root[4][0][6][1][2])
    for row in range(revenue_rows_number):
        revenue_values = []
        for child in root[4][0][6][1][2][row][1]:
            if child[0].tag == 'Value':
                try:
                    revenue_values.append(float(child[0].text))
                except:
                    revenue_values.append(child[0].text)
            else:
                revenue_values.append(0)
        writer.writerow(revenue_values)

    expences_title = root[4][0][6][2][1].text
    print(expences_title)
    writer.writerow("\n")
    writer.writerow([expences_title])

    expences_rows_number = len(root[4][0][6][2][2])
    for row in range(expences_rows_number):
        expences_values = []
        for child in root[4][0][6][2][2][row][1]:
            if child[0].tag == 'Value':
                try:
                    expences_values.append(float(child[0].text))
                except:
                    expences_values.append(child[0].text)
            else:
                expences_values.append(0)
        writer.writerow(expences_values)

    assets_title = root[4][0][6][3][1].text
    print(assets_title)
    writer.writerow("\n")
    writer.writerow([assets_title])

    assets_rows_number = len(root[4][0][6][3][2])
    for row in range(assets_rows_number):
        assets_values = []
        for child in root[4][0][6][2][2][row][1]:
            if child[0].tag == 'Value':
                try:
                    assets_values.append(float(child[0].text))
                except:
                    assets_values.append(child[0].text)
            else:
                assets_values.append(0)
        writer.writerow(assets_values)

    liabilities_title = root[4][0][6][4][1].text
    print(liabilities_title)
    writer.writerow("\n")
    writer.writerow([liabilities_title])

    liabilities_rows_number = len(root[4][0][6][4][2])
    for row in range(liabilities_rows_number):
        liabilities_values = []
        for child in root[4][0][6][2][2][row][1]:
            if child[0].tag == 'Value':
                try:
                    liabilities_values.append(float(child[0].text))
                except:
                    liabilities_values.append(child[0].text)
            else:
                liabilities_values.append(0)
        writer.writerow(liabilities_values)

    equity_title = root[4][0][6][5][1].text
    print(equity_title)
    writer.writerow("\n")
    writer.writerow([equity_title])

    equity_rows_number = len(root[4][0][6][4][2])
    for row in range(equity_rows_number):
        equity_values = []
        for child in root[4][0][6][2][2][row][1]:
            if child[0].tag == 'Value':
                try:
                    equity_values.append(float(child[0].text))
                except:
                    equity_values.append(child[0].text)
            else:
                equity_values.append(0)
        writer.writerow(equity_values)

    trial_balance_csv.close()