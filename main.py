from selenium import webdriver

import re
import time
import copy
import configparser

# My packages
import parser
import amazon_nav
import matcher

# Use encrypted secrets config

config = configparser.ConfigParser()
config.read("secrets/credentials.ini")
myConfig = config['DEFAULT']
otpSecret = myConfig["otpSecret"]
userEmail = myConfig["userEmail"]
userPassword = myConfig["userPassword"]

def main():
    myDriver = webdriver.Chrome()
    amazon_nav.signIn(myDriver, userEmail, userPassword, otpSecret)
    orderIDs = amazon_nav.getAllOrderIDs(myDriver)
    for orderID in orderIDs:
        iPage = amazon_nav.getInvoicePage(myDriver, orderID)
        afterTaxItems, transactions = parser.parseInvoicePage(iPage)
        if afterTaxItems == None or transactions == None:
            continue
        matched = matcher.matchItems(afterTaxItems, transactions)
        print(afterTaxItems, transactions, matched)


if __name__ == "__main__":
    main()