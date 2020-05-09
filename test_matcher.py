from matcher import *
from util import *
import re

# TODO: Fix up these tests.
def testMatchItems():
    a = [("a", 2), ("b", 6), ("c", 12.53), ("d", 1.12), ("e", 3.25), ("f", 8.23)]
    q = round(2+12.53+8.23,2)
    b = [1.12, 9.25, q]
    # res = {9.25: {"e", "b"}, 1.12: {"d"}, q: {"a", "c", "f"}}
    print(matchItems(a,b))

    # TODO: following is an example of a failure
    same = [("a", 5), ("b", 5)]
    cc = [5, 5]
    print(matchItems(same, cc))


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