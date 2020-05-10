'''
    afterTaxItems: [(itemName, afterTaxPrice)]
    transactions: [creditCardTransaction]
'''
# TODO: improve this algorithm and test for correctness
def matchAmazonTransactions(afterTaxItems, transactions):
    result = {}
    if len(transactions) == 1:
        # Easy case we can hack some correctness into
        result[transactions[0]] = list(map(lambda x: x[0], afterTaxItems))
        return result
    itemsPriceComboMap = getItemsCombination(afterTaxItems)
    # Round all items because floating point math
    for price in transactions:
        result[price] = itemsPriceComboMap[price]
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
            # Truncate Items.
            truncatedTransactions = list(map(lambda x: " ".join(x.split()[:3]), at[amtInCents]))
            patch.append({"id": yt["id"], "memo": "|".join(truncatedTransactions)})
            matched = True
      if not matched:
          print (f"Transaction of amt {amtInCents} not matched to any amazon order")
  return patch