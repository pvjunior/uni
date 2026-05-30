def main():
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

    calc(e, x, a, t)

def calc(e: list, x: list, a: list, t: list):
    nStations = len(a[0])
    
    table = [[0 for _ in range(nStations)] for _ in range(2)]

    for vIndex in range(2):
        table[vIndex][0] = e[vIndex] + a[vIndex][0]

    for hIndex in range(1, nStations):
        for vIndex in range(2):
            
            sameLine = table[vIndex][hIndex - 1] + a[vIndex][hIndex]
            
            prevRow = 1 - vIndex
            otherLine = table[prevRow][hIndex - 1] + t[prevRow][hIndex] + a[vIndex][hIndex]

            if sameLine < otherLine:
                table[vIndex][hIndex] = sameLine
            else:
                table[vIndex][hIndex] = otherLine

    for row in table:
        print(row)

    finalCost0 = table[0][-1] + x[0]
    finalCost1 = table[1][-1] + x[1]
    
    print(f"Custo mínimo total: {min(finalCost0, finalCost1)}")

main()