'''
    afterTaxItems: [(itemName, afterTaxPrice)]
    transactions: [creditCardTransaction]
'''
def matchItems(afterTaxItems, transactions):
    # TODO: improve this algorithm and test for correctness
    itemsPriceComboMap = getItemsCombination(afterTaxItems)
    result = {}
    # Round all items because floating point math
    new = {}
    for k, v in itemsPriceComboMap.items():
        new[round(k, 2)] = v
    for price in transactions:
        result[price] = new[price]
    return result

# Amber contributed this nice algorithm which will break if 
# there are different combinations that match the same transaction value
# TODO: Fix this
def getItemsCombination(afterTaxItems):
    if len(afterTaxItems) == 1:
        return {afterTaxItems[0][1]: [afterTaxItems[0][0]]}
    prevCombinations = getItemsCombination(afterTaxItems[:-1])
    curItem = afterTaxItems[-1]
    prices = list(prevCombinations.keys())
    for price in prices:
        prevCombinations[price+curItem[1]] = prevCombinations[price] + [curItem[0]]
        prevCombinations[curItem[1]] = [curItem[0]]
    return prevCombinations

'''
    amazonT: [{ccTransactionInCents: [purchasedItems]}, ...]
    ynabT: [{"id": transactionID, "memo": existingMemo, "amount": amtInCents, ...}]

    return: [{"id": transactionID}, "memo": purchasedItems]
'''
def matchAmazonToYNAB(amazonTransactions, ynabTransactions):
  print(f"amazon: {amazonTransactions}\n\n ynab: {ynabTransactions}")
  patch = []
  for yt in ynabTransactions:
      amtInCents = -yt["amount"]
      matched = False
      for at in amazonTransactions:
        if amtInCents in at:
            # We have a match!
            patch.append({"id": yt["id"], "memo":",".join(at[amtInCents])})
            matched = True
      if not matched:
          print (f"Transaction of amt {amtInCents} not matched to any amazon order")
  return patch