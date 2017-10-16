import csv
from bs4 import BeautifulSoup

def parse_xml(xml_content):
    soup = BeautifulSoup(xml_content,'xml')
    return soup

def open_csv(csv_filename):
    with open(csv_filename+'.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        return writer

def trial_balance_parser(xml_content):
    soup = parse_xml(xml_content)
    header_tags = soup.find("RowType", text="Header").parent.find_all('Value')
    header_text = tuple([h.text for h in header_tags])

    """revenue_tags = soup.find("Title", text="Revenue").next_siblings.find_all('Cell')
    for r in revenue_tags:
        if 'cell' in r:
          #  next(r)
            print(r)
            #if '<Value>' in r:
            #    print(r)
            #else:
            #    print("\n")
    """
    #revenue_tags = soup.find("Rows", text="Revenue").previous_element
    #print(revenue_tags)
    revenue_tags = soup.find("Title", text="Revenue").find_parent('Row')
    #print(r)
    for r in revenue_tags.find_all('Cell'):
        print(r.Value)

    with open('Masedi Electric Serve - Trial Balance.csv', 'w') as csv_file:
        writer = csv.writer(csv_file)
        writer.writerow(header_text)