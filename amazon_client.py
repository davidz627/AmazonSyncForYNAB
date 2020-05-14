import pyotp
from bs4 import BeautifulSoup
import time
import requests

# TODO: https://stackoverflow.com/questions/11892729/how-to-log-in-to-a-website-using-pythons-requests-module/17633072#17633072
# maybe log in with this

class Amazon(object):        
    ORDERS_PAGE = "https://www.amazon.com/gp/css/summary/print.html/ref=ppx_yo_dt_b_invoice_o00?ie=UTF8&orderID={}"

    def __init__(self):
        self.session = requests.Session()
        self.session.headers = {
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/81.0.4044.92 Safari/537.36',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Referer': 'https://www.amazon.com/ap/signin',
            'Origin': "https://www.amazon.com",
            'Ect': "4g",
            'Downlink': "10",
            'Content-Type': 'application/x-www-form-urlencoded',
            'Cache-Control': 'max-age=0',
            'Upgrade-Insecure-Requests': '1',
            'Rtt': "0",
            'Sec-Fetch-Dest': 'document',
            'Sec-Fetch-Mode': 'navigate',
            'Sec-Fetch-Site': 'same-origin',
            'Sec-Fetch-User': '?1',
        }
        for cookie in self.getCookies():
            self.session.cookies.set(**cookie)


    def getCookies(self):
        allCookies = []
        with open("secrets/cookies.txt", "r") as f:
            for line in f:
                tok = line.split(" ")
                cookie = dict()
                cookie["name"] = tok[0]
                cookie["value"] = tok[1]
                cookie["domain"] = tok[2]
                cookie["expires"] = "2225079417" # Some time in 2040
                allCookies.append(cookie)
        return allCookies

    def getAllOrderIDs(self):
        #page = self.session.get("https://www.amazon.com/gp/css/order-history")
        with open("html.txt", "r") as f:
            page = f.read()
            #TODO: The actual page is fucked. For some reason bs can't parse it, we might as well just grep on bdi lol
            soup = BeautifulSoup(page, 'html.parser')
            print(soup.getText())
        #with open("html.txt", "w+") as f:
        #    f.write(str(page.text))
            return [i.getText() for i in soup.find_all("bdi")]

    def deprecatedSignIn(self, driver, userEmail, userPassword, otpSecret):
        totp = pyotp.TOTP(otpSecret)

        driver.get("https://amazon.com")
        accountNav = driver.find_element_by_id("nav-link-accountList")
        accountNav.click()
        
        time.sleep(1)

        emailEntry = driver.find_element_by_id("ap_email")
        emailEntry.clear()
        emailEntry.send_keys(userEmail)
        driver.find_element_by_id("continue").click()

        time.sleep(1)

        passwordEntry =driver.find_element_by_id("ap_password")
        passwordEntry.clear()
        passwordEntry.send_keys(userPassword)
        driver.find_element_by_name("rememberMe").click()
        driver.find_element_by_id("signInSubmit").click()

        time.sleep(1)

        otpEntry = driver.find_element_by_id("auth-mfa-otpcode")
        otpEntry.clear()
        otpEntry.send_keys(totp.now())
        driver.find_element_by_id("auth-mfa-remember-device").click()
        driver.find_element_by_id("auth-signin-button").click()

        time.sleep(1)

    def getInvoicePage(self, orderID):
        myOrderPage = self.ORDERS_PAGE.format(orderID)
        page = self.session.get(myOrderPage)
        return page.text