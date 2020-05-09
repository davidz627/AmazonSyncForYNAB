import requests
import json
import re

class YNAB(object):
    BASE_URL = "https://api.youneedabudget.com/v1"

    def __init__(self, token, budgetID):
        self.budgetID = budgetID
        self.headers = {
            "Authorization": f"Bearer {token}",
            "accept": "application/json",
        }

    # TODO: Make date range based on current date
    # TODO: Make budget ID configurable
    def list_recent_amazon_transactions(self):
        #url = self.BASE_URL + "/budgets/6d515631-e0bc-43a2-bba6-a4242dfe307d/transactions?since_date=2020-04-03&type=uncategorized"
        url = self.BASE_URL + "/budgets/6d515631-e0bc-43a2-bba6-a4242dfe307d/transactions?since_date=2020-05-04"
        rawResponse = requests.get(url ,headers=self.headers)
        resp = json.loads(rawResponse.content.decode('utf-8'))
        if rawResponse.status_code != 200:
            return None
        transactions = resp["data"]["transactions"]
        amazon = re.compile(r"[[aA]mazon|AMZN]")
        memo = re.compile(r"[Amazon|AMZN].*\*[\d|A-Z]+")
        memoFilter = filter(lambda item: item["memo"] == None or memo.match(item["memo"]), transactions)
        onlyAmazon = filter(lambda item: amazon.match(item["payee_name"]),memoFilter)
        return list(onlyAmazon)