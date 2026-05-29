value = 6
available = [1, 3, 4]

table = [[-1 for _ in range(value)] for _ in available]
    

memoization(value, available)

def memoization(val, ava):
    currRow = len(ava) - 1
    lCoinAva = ava[-1]
    lastBestOption = getChange(value, currRow - 1)

    if lCoinAva > val:
        table[currRow][value - 1]


def getChange(val: int, row: int) -> list:
    if table[row][val - 1] == 0:
        memoization(val, available[:row])

    return table[row][val - 1]



