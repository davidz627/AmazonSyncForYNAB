import re
from bs4 import BeautifulSoup

def parseInvoicePage(page_source):
    pageSoup = BeautifulSoup(page_source, "html.parser")
    itemNames = pageSoup.find_all("i") # Dirty hack: names are the only thing in italics lmao
    items = []
    for item in itemNames:
        numItems = int(item.parent.text.split()[0])
        itemName = item.text
        itemValue = float(item.parent.parent.findAll("td")[1].text.strip()[1:])
        items.append((itemName, itemValue*numItems))

    beforeTax = float(pageSoup.find(text=re.compile(r"Total before tax")).parent.parent.findAll("td")[1].text.strip()[1:])
    tax= float(pageSoup.find(text=re.compile(r"Estimated tax to be collected")).parent.parent.findAll("td")[1].text.strip()[1:])
    if beforeTax <= 0:
        print(f"Before tax value is less than or equal to 0, was {items} free?")
        return None, None
    taxPercent = tax/beforeTax
    afterTaxItems = [(i[0], round(i[1]*(1+taxPercent), 2)) for i in items]

    #Then get "Credit Card Transactions"
    transactions = None
    ccTransactions = pageSoup.find(text=re.compile(r"Credit Card transactions"))
    if ccTransactions == None:
        print(f"No Credit Card Transactions line item found, maybe {afterTaxItems} haven't been paid for yet")
        return None, None

    transactionsContainer = ccTransactions.parent.parent.parent.parent
    transactions = transactionsContainer.findAll(text=re.compile(r"\$\d+"))
    transactions = [float(t.strip()[1:]) for t in transactions]

    return afterTaxItems, transactions