from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
import re
import time
import copy
import configparser

# My packages
import parser
import amazon_nav
import matcher
from ynab_client import YNAB
# from amazon_client import Amazon

# Use encrypted secrets config

config = configparser.ConfigParser()
config.read("secrets/credentials.ini")
myConfig = config['DEFAULT']
otpSecret = myConfig["otpSecret"]
userEmail = myConfig["userEmail"]
userPassword = myConfig["userPassword"]
ynabToken = myConfig["ynabToken"]

def main():
    options = Options()
    # options.add_argument('--headless')
    myDriver = webdriver.Chrome(ChromeDriverManager().install(), chrome_options=options)
    amazon_nav.signIn(myDriver, userEmail, userPassword, otpSecret)
    orderIDs = amazon_nav.getAllOrderIDs(myDriver)
    amazonT = []
    for orderID in orderIDs:
        try:
            iPage = amazon_nav.getInvoicePage(myDriver, orderID)
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
    main()