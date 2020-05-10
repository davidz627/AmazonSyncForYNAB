from matcher import *
from util import *
import re

# TODO: Fix up these tests.
def testmatchAmazonTransactions():
    tests = {
        "simple": {
            "items": [("a", 200), ("b", 600), ("c", 1253), ("d", 112), ("e", 325), ("f", 823)],
            "transactions": [112, 925, 2276],
            "expMatch": {925: ["e", "b"], 112: ["d"], 2276: ["a", "c", "f"]}
        },
        "oneItemNoMatchCost": {
            "items": [("a", 200)],
            "transactions": [100],
            "expMatch": {100: ["a"]}
        },
    }
    for testName, tc in tests.items():
        print (f"running test {testName}")
        assert equalsEnough(matchAmazonTransactions(tc["items"], tc["transactions"]), tc["expMatch"])

    # TODO: following is an example of a failure
    #same = [("a", 5), ("b", 5)]
    #cc = [5, 5]
    #print(matchAmazonTransactions(same, cc))


def testMatchAmazonToYNAB():
    tests = {
        "works": {
            "amazonT":[{503: ["blob"], 103: ["oboe"]}],
            "ynabT": [{"id": 123, "memo": "foo", "amount":-503},{"id": 321, "amount":-103}],
            "expPatch": [{"id": 321, "memo": "oboe"}, {"id": 123, "memo": "blob"}],
        },
        "works multiple transactions": {
            "amazonT":[{503: ["blob"]}, {103: ["oboe"]}],
            "ynabT": [{"id": 123, "memo": "foo", "amount":-503},{"id": 321, "amount":-103}],
            "expPatch": [{"id": 321, "memo": "oboe"}, {"id": 123, "memo": "blob"}],
        },
        "notAllInYNAB":{
            "amazonT":[{503: ["blob"], 103: ["oboe"]}],
            "ynabT": [{"id": 321, "amount":-103}],
            "expPatch": [{"id": 321, "memo": "oboe"}],
        },
        "notAllInAmazon":
            {
            "amazonT":[{503: ["blob"]}],
            "ynabT": [{"id": 123, "memo": "foo", "amount":-503},{"id": 321, "amount":-103}],
            "expPatch": [{"id": 123, "memo": "blob"}],
        },
    }

    for testName, tc in tests.items():
        print(f"running test {testName}")
        patch = matchAmazonToYNAB(tc["amazonT"], tc["ynabT"])
        assert equalsEnough(patch, tc["expPatch"]) == True