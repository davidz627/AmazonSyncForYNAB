from selenium import webdriver
import pyotp
import re
from bs4 import BeautifulSoup
import time
import copy
import configparser

# Use encrypted secrets config

config = configparser.ConfigParser()
config.read("secrets/credentials.ini")
myConfig = config['DEFAULT']
orderPage = "https://www.amazon.com/gp/css/summary/print.html/ref=ppx_yo_dt_b_invoice_o00?ie=UTF8&orderID={}"
otpSecret = myConfig["otpSecret"]
userEmail = myConfig["userEmail"]
userPassword = myConfig["userPassword"]

def getAllOrderIDs(driver):
    driver.get("https://www.amazon.com/gp/css/order-history")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return [i.getText() for i in soup.find_all("bdi")]

def signIn(driver):

    totp = pyotp.TOTP(otpSecret)

    driver.get("https://amazon.com")
    accountNav = driver.find_element_by_id("nav-link-accountList")
    accountNav.click()

    emailEntry = driver.find_element_by_id("ap_email")
    emailEntry.clear()
    emailEntry.send_keys(userEmail)
    driver.find_element_by_id("continue").click()

    passwordEntry =driver.find_element_by_id("ap_password")
    passwordEntry.clear()
    passwordEntry.send_keys(userPassword)
    driver.find_element_by_name("rememberMe").click()
    driver.find_element_by_id("signInSubmit").click()

    otpEntry = driver.find_element_by_id("auth-mfa-otpcode")
    otpEntry.clear()
    otpEntry.send_keys(totp.now())
    driver.find_element_by_id("auth-mfa-remember-device").click()
    driver.find_element_by_id("auth-signin-button").click()

def getInvoicePage(driver, orderID):
    myOrderPage = orderPage.format(orderID)
    driver.get(myOrderPage)
    return driver.page_source

def parseInvoicePage(page_source):
    pageSoup = BeautifulSoup(page_source, "html.parser")
    itemNames = pageSoup.find_all("i") # Dirty hack: names are the only thing in italics lmao
    items = []
    for item in itemNames:
        itemName = item.text
        itemValue = float(item.parent.parent.findAll("td")[1].text.strip()[1:])
        items.append((itemName, itemValue))

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

'''
    afterTaxItems: [(itemName, afterTaxPrice)]
    transactions: [creditCardTransaction]
'''
def matchItems(afterTaxItems, transactions):
    # TODO: improve this algorithm and test for correctness
    itemsPriceComboMap = getItemsCombination(afterTaxItems)
    result = {}
    # Round all items because floating point math
    new = {}
    for k, v in itemsPriceComboMap.items():
        new[round(k, 2)] = v
    for price in transactions:
        result[price] = new[price]
    return result

# Amber contributed this nice algorithm which will break if 
# there are different combinations that match the same transaction value
# TODO: Fix this
def getItemsCombination(afterTaxItems):
    if len(afterTaxItems) == 1:
        return {afterTaxItems[0][1]: [afterTaxItems[0][0]]}
    prevCombinations = getItemsCombination(afterTaxItems[:-1])
    curItem = afterTaxItems[-1]
    prices = list(prevCombinations.keys())
    for price in prices:
        prevCombinations[price+curItem[1]] = prevCombinations[price] + [curItem[0]]
        prevCombinations[curItem[1]] = [curItem[0]]
    return prevCombinations

# test()

myDriver = webdriver.Chrome()
signIn(myDriver)
orderIDs = getAllOrderIDs(myDriver)
firstOrderID = "112-3232573-1284263"
for orderID in orderIDs:
   iPage = getInvoicePage(myDriver, orderID)
   afterTaxItems, transactions = parseInvoicePage(iPage)
   if afterTaxItems == None or transactions == None:
       continue
   matched = matchItems(afterTaxItems, transactions)
   print(afterTaxItems, transactions, matched)
