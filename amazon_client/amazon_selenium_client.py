import pyotp
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options
from amazon_client import AmazonClient

ORDERS_PAGE = "https://www.amazon.com/gp/css/summary/print.html/ref=ppx_yo_dt_b_invoice_o00?ie=UTF8&orderID={}"

class AmazonSeleniumClient(AmazonClient):
    def __init__(self, userEmail, userPassword, otpSecret):
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.otpSecret = otpSecret
        options = Options()
        options.add_argument('--headless')
        self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
        self.signIn()

    def getAllOrderIDs(self):
        self.driver.get("https://www.amazon.com/gp/css/order-history")
        soup = BeautifulSoup(self.driver.page_source, 'html.parser')
        return [i.getText() for i in soup.find_all("bdi")]

    def signIn(self):
        totp = pyotp.TOTP(self.otpSecret)

        self.driver.get("https://amazon.com")
        accountNav = self.driver.find_element_by_xpath("//a[@data-nav-role='signin']")
        accountNav.click()
        # data-nav-role="signin"
        time.sleep(1)

        emailEntry = self.driver.find_element_by_id("ap_email")
        emailEntry.clear()
        emailEntry.send_keys(self.userEmail)
        self.driver.find_element_by_id("continue").click()

        time.sleep(1)

        passwordEntry =self.driver.find_element_by_id("ap_password")
        passwordEntry.clear()
        passwordEntry.send_keys(self.userPassword)
        self.driver.find_element_by_name("rememberMe").click()
        self.driver.find_element_by_id("signInSubmit").click()

        time.sleep(1)

        otpEntry = self.driver.find_element_by_id("auth-mfa-otpcode")
        otpEntry.clear()
        otpEntry.send_keys(totp.now())
        self.driver.find_element_by_id("auth-mfa-remember-device").click()
        self.driver.find_element_by_id("auth-signin-button").click()

        time.sleep(1)

    def getInvoicePage(self, orderID):
        myOrderPage = ORDERS_PAGE.format(orderID)
        self.driver.get(myOrderPage)
        return self.driver.page_source