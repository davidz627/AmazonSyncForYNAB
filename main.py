import re
import time
import copy
import configparser

# My packages
import parser
import matcher
from ynab_client import YNABClient
from amazon_client.amazon_selenium_client import AmazonSeleniumClient
from datetime import date, timedelta

# TODO: Use encrypted secrets config
config = configparser.ConfigParser()
config.read("secrets/credentials.ini")
myConfig = config['DEFAULT']
otpSecret = myConfig["otpSecret"]
userEmail = myConfig["userEmail"]
userPassword = myConfig["userPassword"]
ynabToken = myConfig["ynabToken"]

def main(amazonClient):
    orderIDs = amazonClient.getAllOrderIDs(3)
    amazonT = []
    for orderID in orderIDs:
        try:
            iPage = amazonClient.getInvoicePage(orderID)
            afterTaxItems, transactions = parser.parseInvoicePage(iPage)
            if afterTaxItems == None or transactions == None:
                continue
            matched = matcher.matchAmazonTransactions(afterTaxItems, transactions)
            amazonT.append(matched)
        except Exception as e:
            print(f"Something went wrong processing order {orderID}: {e}")
    myYNAB = YNABClient(ynabToken)
    ynabT = myYNAB.list_recent_amazon_transactions(date.today() - timedelta(days=180))
    transactions = matcher.matchAmazonToYNAB(amazonT, ynabT)
    myYNAB.patch_transactions(transactions)


if __name__ == "__main__":
    amazonSeleniumClient = AmazonSeleniumClient(userEmail, userPassword, otpSecret)
    main(amazonSeleniumClient)