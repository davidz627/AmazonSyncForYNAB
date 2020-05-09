from matcher import *

# def testParseInvoicePage():
#     f = open("tet/orders/simpleOrder.html", "r")
#     page = f.read()
#     afterTaxItems, transactions = parseInvoicePage(page)
#     matched = matchItems(afterTaxItems, transactions)
#     print(afterTaxItems, transactions)
#     f.close() 

def testMatchItems():
# TODO: How to actually run tests in a reasonable way? pytest?
    a = [("a", 2), ("b", 6), ("c", 12.53), ("d", 1.12), ("e", 3.25), ("f", 8.23)]
    q = round(2+12.53+8.23,2)
    b = [1.12, 9.25, q]
    # res = {9.25: {"e", "b"}, 1.12: {"d"}, q: {"a", "c", "f"}}
    print(matchItems(a,b))

    # TODO: following is an example of a failure
    same = [("a", 5), ("b", 5)]
    cc = [5, 5]
    print(matchItems(same, cc))