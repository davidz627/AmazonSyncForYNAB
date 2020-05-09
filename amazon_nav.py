import pyotp
from bs4 import BeautifulSoup

ORDERS_PAGE = "https://www.amazon.com/gp/css/summary/print.html/ref=ppx_yo_dt_b_invoice_o00?ie=UTF8&orderID={}"

def getAllOrderIDs(driver):
    driver.get("https://www.amazon.com/gp/css/order-history")
    soup = BeautifulSoup(driver.page_source, 'html.parser')
    return [i.getText() for i in soup.find_all("bdi")]

def signIn(driver, userEmail, userPassword, otpSecret):
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
    myOrderPage = ORDERS_PAGE.format(orderID)
    driver.get(myOrderPage)
    return driver.page_source