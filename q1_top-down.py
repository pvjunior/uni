value = 6
available = [1, 3, 4]

table = [[0 for _ in range(value)] for _ in available]


print(table)


def memoization(val, ava):
    currRow = len(ava) - 1
    currTableCell = table[currRow][val - 1] 
    print(f"lca: {ava}[-1]")
    print(f" val: {val} ---- currRow: {currRow} ----")
    lCoinAva = ava[-1]
    print(f"currRow: {currRow}")
    lastBestOption = getChange(val, currRow - 1) if currRow - 1 else [1]
    print(f"lbo: {lastBestOption} --- val: {val} ---- currRow: {currRow} ---- lCA: {lCoinAva}")

    if lCoinAva > val:
        currTableCell = lastBestOption
        return
    
    val -= lCoinAva
    change = []
    change.append(lCoinAva)

    if val:
        change.append(getChange(val, currRow))
    
        print(lastBestOption)
    if len(lastBestOption) < len(change):
        change = lastBestOption

    currTableCell = change


def getChange(val: int, row: int) -> list:

    if table[row][val - 1] == 0:
        print(f"no value in table[{row}][{val - 1}] (value: {val}) --- running mem({val}, {available}[:{row}])  resava: {available[:row]}")
        memoization(val, available[:row])

    return table[row][val - 1]


memoization(value, available)

for row in table:
    print(row)
