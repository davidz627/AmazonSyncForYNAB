import pyotp
from bs4 import BeautifulSoup
import time
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.chrome.options import Options as ChromeOptions
from amazon_client.amazon_client import AmazonClient
import platform

ORDERS_PAGE = "https://www.amazon.com/gp/css/summary/print.html/ref=ppx_yo_dt_b_invoice_o00?ie=UTF8&orderID={}"

class AmazonSeleniumClient(AmazonClient):
    def __init__(self, userEmail, userPassword, otpSecret):
        self.userEmail = userEmail
        self.userPassword = userPassword
        self.otpSecret = otpSecret
        platformMachine = platform.machine()
        if platformMachine == "armv7l":
            # TODO: Raspberry Pi: Support this somehow. Webdriver installation needs to be bespoke
            err = "Platform {} not yet supported".format(platformMachine)
            print(err)
            exit(0)
        else:
            print(f"Attempting to initialize Chrome Selenium Webdriver on platform {platformMachine}...")
            options = ChromeOptions()
            options.add_argument('--headless')
            self.driver = webdriver.Chrome(ChromeDriverManager().install(), options=options)
            print("Successfully initialize Chrome Selenium Webdriver")

        self.signIn()

    def getAllOrderIDs(self, pages=1):
        orderPage = "https://www.amazon.com/gp/your-account/order-history/ref=ppx_yo_dt_b_pagination_1_2?ie=UTF8&orderFilter=months-6&search=&startIndex={}"
        orderIDs = []
        for pageNumber in range(pages):
            self.driver.get(orderPage.format(pageNumber * 10))
            soup = BeautifulSoup(self.driver.page_source, 'html.parser')
            orderIDs.extend([i.getText() for i in soup.find_all("bdi")])
        return orderIDs

    def signIn(self):
        # TODO: Wait for page load instead of sleeping so much
        totp = pyotp.TOTP(self.otpSecret)

        self.driver.get("https://amazon.com")
        time.sleep(1)
        accountNav = self.driver.find_element_by_xpath("//a[@data-nav-role='signin']")
        accountNav.click()
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
