value = 6
available = [1, 3, 4]

table = [[0 for _ in range(value)] for _ in available]


print(table)


def memoization(val, ava):
    currRow = len(ava) - 1
    lCoinAva = ava[-1]
    lastBestOption = getChange(val, currRow - 1) if currRow - 1 else [1]
    if val == 3:
        print(f"15. table[row][val - 1] ==== {table[currRow][val - 1]} ----- val: {val} ---- row: {currRow}")
    if lCoinAva > val:
        table[currRow][val - 1] = lastBestOption
        print(f"{table[currRow][val - 1]}")
        return
    targetVal = val
    targetVal -= lCoinAva
    change = []
    change.append(lCoinAva)

    if targetVal:
        print(f"25. shuii shuuii: {getChange(targetVal, currRow)}")
        change.extend(getChange(targetVal, currRow))
    

    if len(lastBestOption) < len(change):
        change = lastBestOption
    if val == 3:
        print(f"33. table[row][val - 1] ==== {table[currRow][val - 1]} ----- val: {val} ---- row: {currRow}")
    table[currRow][val - 1] = change
    print(f"34. MANOOO: {table[currRow][val - 1]}")

def getChange(val: int, row: int) -> list:

    if table[row][val - 1] == 0:
        print(f"38. table[row][val - 1] ==== {table[row][val - 1]} ----- val: {val} ---- row: {row}")
        memoization(val, available[:row + 1])

    if table[row][val - 1] == 0:
        print(f"41. parece que é 0 dnv")
    return table[row][val - 1]


memoization(value, available)

for row in table:
    print(row)
