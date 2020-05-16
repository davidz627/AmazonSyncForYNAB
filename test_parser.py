from parser import parseInvoicePage
from util import equalsEnough

def testParseInvoicePage():
    tests = {
        "simple": {
            "filename": "test/orders/simpleOrder.html",
            "expAfterTaxItems": [('Glad Tall Kitchen Drawstring Trash Bags - OdorShield 13 Gallon White Trash Bag, Febreze Fresh Clean - 110 Count', 1776), ('Crest ProHealth Advanced Mouthwash With Extra Whitening Energizing Mint Flavor 16 fl oz. Pack of 4', 2600)],
            "expTransactions": [1776, 2600]
        },
        # We make an explicit assumption that 2 items will always
        # be on the same card charge here for simplicity
        # This may not always be true but should be fine for now...
        "twoOfSameItem": {
            "filename": "test/orders/twoOfSameItem.html",
            "expAfterTaxItems": [("CeraVe", 3256)],
            "expTransactions": [3256]
        },
        "fourDifferentItems": {
            "filename": "test/orders/fourDifferentItems.html",
            "expAfterTaxItems": [('Foam', 1387), ('Suptikes', 1084), ('6 Pack Stainless', 650), ('Escali', 2169)],
            "expTransactions": [5290]
        },
    }
    for testName, tc in tests.items():
        with open(tc["filename"], "r") as f:
            page = f.read()
            afterTaxItems, transactions = parseInvoicePage(page)
            assert equalsEnough(afterTaxItems, tc["expAfterTaxItems"])
            assert equalsEnough(transactions, tc["expTransactions"])