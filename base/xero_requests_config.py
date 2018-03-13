import requests
from datetime import datetime

class XeroRequestsDef():

    def __init__(self, authenticate):
        self.authenticate = authenticate

    def xero_get_request(self,api_url, date_range=None):
        content = requests.get(url=api_url, auth=self.authenticate.oauth, params=date_range)
        return content.text

    def trial_balance_as_at_date(self, as_date):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/TrialBalance'
        date_range = {'date': datetime.strptime(as_date,'%Y-%m-%d')}
        return self.xero_get_request(api_url, date_range)

    def balance_sheet_as_at_date(self, as_date):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/BalanceSheet'
        date_range = {'date': datetime.strptime(as_date,'%Y-%m-%d')}
        return self.xero_get_request(api_url, date_range)

    def profit_loss_from_to_date(self, fromDate, toDate):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/ProfitAndLoss'
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url,date_range)

    def aged_payables_from_to_date(self,fromDate, toDate, contactID):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/AgedPayablesByContact?ContactID='+contactID
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url,date_range)

    def contact_ids(self):
        api_url = 'https://api.xero.com/api.xro/2.0/Contacts'
        contacts = requests.get(url=api_url, auth=self.authenticate.oauth)
        return contacts.text

    def aged_receivables_from_to_date(self, fromDate, toDate, contactID):
        api_url = 'https://api.xero.com/api.xro/2.0/Reports/AgedReceivablesByContact?ContactID='+contactID
        date_range = {'fromDate': fromDate, 'toDate': toDate}
        return self.xero_get_request(api_url, date_range)

    def get_invoices(self):
        #api_url = "https://api.xero.com/api.xro/2.0/Invoices?where=Date%20%3E%3D%20DateTime%282017%2C%2001%2C%2001%29%20%26%26%20Date%20%3C%20DateTime%282017%2C%2012%2C%2031%29"
        api_url = "https://api.xero.com/api.xro/2.0/Accounts"
        return self.xero_get_request(api_url)

    def get_credit_notes(self):
        api_url="https://api.xero.com/api.xro/2.0/CreditNotes"
        return self.xero_get_request(api_url)

    def put_invoices(self, put_xml):
        api_url="https://api.xero.com/api.xro/2.0/Invoices"
        xml_data="""<Invoice>
  <Type>ACCPAY</Type>
  <Contact>
    <ContactID>75f5f830-41ad-47f6-9685-f5044b885106</ContactID>
  </Contact>
  <InvoiceNumber>INV03403</InvoiceNumber>
  <Reference>Johannesburg</Reference>
  <Date>2017-04-03</Date>
  <DueDate>2017-05-03</DueDate>
  <Status>AUTHORISED</Status>
  <LineItems>
    <LineItem>
      <Description>Material</Description>
      <Quantity>1.0000</Quantity>
      <UnitAmount>3212.29</UnitAmount>
      <TaxAmount>394.49</TaxAmount>
      <AccountCode>312</AccountCode>
    </LineItem>
  </LineItems>
</Invoice>"""

        """<Invoice>
  <Type>ACCPAY</Type>
  <Contact>
    <ContactID>75f5f830-41ad-47f6-9685-f5044b885106</ContactID>
  </Contact>
      <InvoiceNumber>INV03382</InvoiceNumber>
  <Reference>Johannesburg</Reference>
  <Date>2017-04-03</Date>
  <DueDate>2017-05-03</DueDate>
  <LineAmountTypes>Exclusive</LineAmountTypes>
  <LineItems>
    <LineItem>
      <Description>Material</Description>
      <Quantity>1.0000</Quantity>
      <UnitAmount>5756.54</UnitAmount>
      <AccountCode>312</AccountCode>
    </LineItem>
  </LineItems>
</Invoice>"""

        """<Invoice>
  <Type>ACCPAY</Type>
  <Contact>
    <ContactID>75f5f830-41ad-47f6-9685-f5044b885106</ContactID>
  </Contact>
  <InvoiceNumber>INV03419</InvoiceNumber>
  <Reference>Johannesburg</Reference>
  <Date>2017-04-01</Date>
  <LineItems>
    <LineItem>
      <Description>Material</Description>
      <UnitAmount>1832.32</UnitAmount>
      <TaxAmount>225.02</TaxAmount>
    </LineItem>
  </LineItems>
</Invoice>"""
        put_request = requests.put(api_url, data=xml_data, auth=self.authenticate.oauth)
        return put_request

    def put_contacts(self, xml_input):
        api_url="https://api.xero.com/api.xro/2.0/Contacts"
        xml_contact="""<Contact>
      <ContactID>bbda519a-0818-4b7c-8be3-0f2bd60b2d10</ContactID>
      <ContactStatus>ACTIVE</ContactStatus>
      <Name>CHICKEN LICKEN</Name>
      <Addresses>
        <Address>
          <AddressType>STREET</AddressType>
        </Address>
        <Address>
          <AddressType>POBOX</AddressType>
        </Address>
      </Addresses>
      <Phones>
        <Phone>
          <PhoneType>DDI</PhoneType>
        </Phone>
        <Phone>
          <PhoneType>DEFAULT</PhoneType>
        </Phone>
        <Phone>
          <PhoneType>FAX</PhoneType>
        </Phone>
        <Phone>
          <PhoneType>MOBILE</PhoneType>
        </Phone>
      </Phones>
      <UpdatedDateUTC>2018-02-26T14:16:33.84</UpdatedDateUTC>
      <IsSupplier>true</IsSupplier>
      <IsCustomer>false</IsCustomer>
      <Balances>
        <AccountsReceivable>
          <Outstanding>0.00</Outstanding>
          <Overdue>0.00</Overdue>
        </AccountsReceivable>
        <AccountsPayable>
          <Outstanding>205.40</Outstanding>
          <Overdue>205.40</Overdue>
        </AccountsPayable>
      </Balances>
      <HasAttachments>false</HasAttachments>
    </Contact>"""
        put_request = requests.put(api_url, data=xml_input, auth=self.authenticate.oauth)
        return put_request








