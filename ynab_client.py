import requests
import json
import re
from datetime import date, timedelta

class YNAB(object):
    BASE_URL = "https://api.youneedabudget.com/v1"

    def __init__(self, token):
        self.token = token
        self.budgetID = self.getBudgetID()

    # TODO: Only gets the 0th budget available.
    # We should eventually check all budgets just in case
    def getBudgetID(self):
        url = self.BASE_URL + "/budgets"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json",
        }
        rawResponse = requests.get(url ,headers=headers)
        resp = json.loads(rawResponse.content.decode('utf-8'))
        return resp["data"]["budgets"][0]["id"]

    def list_recent_amazon_transactions(self):
        todayDate = date.today() - timedelta(days=30)
        priorDateStr = todayDate.strftime("%Y-%m-%d")
        url = self.BASE_URL + f"/budgets/{self.budgetID}/transactions?since_date={priorDateStr}"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json",
        }
        rawResponse = requests.get(url ,headers=headers)
        resp = json.loads(rawResponse.content.decode('utf-8'))
        if rawResponse.status_code != 200:
            return None
        transactions = resp["data"]["transactions"]
        amazon = re.compile(r"[[aA]mazon|AMZN]")
        onlyAmazon = filter(lambda item: amazon.match(item["payee_name"]),transactions)
        onlyAmazon = list(onlyAmazon)
        for i in range(len(onlyAmazon)):
            onlyAmazon[i]["amount"] = onlyAmazon[i]["amount"]//10
        return list(onlyAmazon)

    '''
        transactions: [{"id": id, ...}]
    '''
    def patch_transactions(self, transactions):
        if len(transactions) == 0:
            print("No transactions to patch, skipping...")
            return
        url = self.BASE_URL + f"/budgets/{self.budgetID}/transactions"
        headers = {
            "Authorization": f"Bearer {self.token}",
            "accept": "application/json",
            "Content-Type": "application/json"
        }
        data = json.dumps({"transactions": transactions})
        resp = requests.patch(url, data, headers=headers)
        print(f"about to patch data: {data}")
        if resp.status_code != 200:
            print (f"Something went wrong, got response: {resp.content}")
        else:
            print (f"Successfully updated transactions {transactions}")