e = [10, 12]
x = [18, 7]
a = [
    [4, 5, 3, 2], 
    [2, 10, 1, 4]
]
t = [
    [0, 7, 4, 5], 
    [0, 9, 2, 8]
]

nStations = len(a[0])
table = [[0 for _ in range(nStations)] for _ in range(2)]

def memoization(currRow: int, hIndex: int):
    if hIndex == 0:
        table[currRow][0] = e[currRow] + a[currRow][0]
        return
    
    sameLine = getTime(currRow, hIndex - 1) + a[currRow][hIndex]
    
    prevRow = 1 - currRow
    otherLine = getTime(prevRow, hIndex - 1) + t[prevRow][hIndex] + a[currRow][hIndex]

    if sameLine < otherLine:
        table[currRow][hIndex] = sameLine
    else:
        table[currRow][hIndex] = otherLine

def getTime(currRow: int, hIndex: int) -> int:
    
    if table[currRow][hIndex] == 0:
        memoization(currRow, hIndex)
        
    return table[currRow][hIndex]

getTime(0, nStations - 1)
getTime(1, nStations - 1)

for row in table:
    print(row)

finalCost0 = table[0][-1] + x[0]
finalCost1 = table[1][-1] + x[1]

print(f"Custo mínimo total: {min(finalCost0, finalCost1)}")