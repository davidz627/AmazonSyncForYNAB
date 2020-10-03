import re
import time
import copy
import configparser

# My packages
import parser
import matcher
from ynab_client import YNAB
from amazon_selenium_client import AmazonSeleniumClient
# from amazon_client import Amazon

# Use encrypted secrets config

config = configparser.ConfigParser()
config.read("secrets/credentials.ini")
myConfig = config['DEFAULT']
otpSecret = myConfig["otpSecret"]
userEmail = myConfig["userEmail"]
userPassword = myConfig["userPassword"]
ynabToken = myConfig["ynabToken"]

def main(amazonClient):
    orderIDs = amazonClient.getAllOrderIDs()
    amazonT = []
    for orderID in orderIDs:
        try:
            iPage = amazonClient.getInvoicePage(orderID)
            afterTaxItems, transactions = parser.parseInvoicePage(iPage)
            if afterTaxItems == None or transactions == None:
                continue
            matched = matcher.matchAmazonTransactions(afterTaxItems, transactions)
            amazonT.append(matched)
            print(afterTaxItems, transactions, matched)
        except Exception as e:
            print(f"Something went wrong processing order {orderID}: {e}")
    myYNAB = YNAB(ynabToken)
    ynabT = myYNAB.list_recent_amazon_transactions()
    transactions = matcher.matchAmazonToYNAB(amazonT, ynabT)
    myYNAB.patch_transactions(transactions)


if __name__ == "__main__":
    amazonSeleniumClient = AmazonSeleniumClient(userEmail, userPassword, otpSecret)
    main(amazonSeleniumClient)