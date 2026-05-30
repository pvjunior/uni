
value = int(input("valor: "))
available = list(map(int, input("moedas: ").split()))


table = [[0 for _ in range(value)] for _ in available]


#print(table)


def memoization(val, ava):
    currRow = len(ava) - 1
    lCoinAva = ava[-1]
    if lCoinAva > val:
        lastBestOption = getChange(val, currRow - 1)
        table[currRow][val - 1] = lastBestOption
        return
    
    targetVal = val
    targetVal -= lCoinAva
    change = []
    change.append(lCoinAva)
    
    if targetVal:
        change.extend(getChange(targetVal, currRow))

    if (currRow != 0) and (len(getChange(val, currRow - 1)) < len(change)):
        change = getChange(val, currRow - 1)
            
    table[currRow][val - 1] = change

def getChange(val: int, row: int) -> list:

    if table[row][val - 1] == 0:
        memoization(val, available[:row + 1])

    return table[row][val - 1]


memoization(value, available)

for row in table:
    print(row)
