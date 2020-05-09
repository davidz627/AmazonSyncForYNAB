from parser import parseInvoicePage
from util import equalsEnough

def testParseInvoicePage():
    tests = {
        "simple": {
            "filename": "test/orders/simpleOrder.html",
            "expAfterTaxItems": [('Glad Tall Kitchen Drawstring Trash Bags - OdorShield 13 Gallon White Trash Bag, Febreze Fresh Clean - 110 Count', 17.76), ('Crest ProHealth Advanced Mouthwash With Extra Whitening Energizing Mint Flavor 16 fl oz. Pack of 4', 26.0)],
            "expTransactions": [17.76, 26.0]
        },
        # We make an explicit assumption that 2 items will always
        # be on the same card charge here for simplicity
        # This may not always be true but should be fine for now...
        "twoOfSameItem": {
            "filename": "test/orders/twoOfSameItem.html",
            "expAfterTaxItems": [("CeraVe", 32.56)],
            "expTransactions": [32.56]
        },
        "fourDifferentItems": {
            "filename": "test/orders/fourDifferentItems.html",
            "expAfterTaxItems": [('Foam', 13.87), ('Suptikes', 10.84), ('6 Pack Stainless', 6.5), ('Escali', 21.69)],
            "expTransactions": [52.90]
        },
    }
    for testName, tc in tests.items():
        print(f"Running test {testName}")
        with open(tc["filename"], "r") as f:
            page = f.read()
            afterTaxItems, transactions = parseInvoicePage(page)
            assert equalsEnough(afterTaxItems, tc["expAfterTaxItems"])
            assert equalsEnough(transactions, tc["expTransactions"])