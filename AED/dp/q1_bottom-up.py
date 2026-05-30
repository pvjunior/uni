
def main():

    while True:
        val = int(input("valor: "))
        ava = list(map(int, input("moedas: ").split()))

        calc(val, ava)

def calc(val: int, ava: list):
    # table[len(ava)][val]
    table = [[0 for _ in range(val)] for _ in range(len(ava))]

    if 1 not in ava:
        print("Sem moeda 1c, melhor n...")
        exit()

    for vIndex, coin in enumerate(ava):
        for hIndex, value in enumerate(range(1, val + 1)):


            if coin > value:
                # Kinda impossible to the coin be bigger than value and not have a previous line
                # This is the last best, calculated, option for this value. The new coin available cannot bring a new best option.
                table[vIndex][hIndex] = table[vIndex - 1][hIndex]
                continue
            
            change = []
            targetChange = value

            # Uses our newest available coin
            change.append(coin)
            changeSum = sum(change)
            targetChange -= changeSum

            if targetChange:
                # Use the best last calculated combination for the remaining value
                change.extend(table[vIndex][targetChange - 1])
            
            # Check if the last best option was better
            if ((vIndex - 1) != -1) and (len(table[vIndex - 1][hIndex]) < len(change)):
                change = table[vIndex - 1][hIndex]


            table[vIndex][hIndex] = change.copy()

    for row in table:
        print(row)

main()