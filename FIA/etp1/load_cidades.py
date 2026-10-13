class cidade():
    def __init__(self, nome: str, dist: int):
        self.nome = nome
        self.dist = dist # distância até POA em linha reta


def load_heuristica(input_file: str) -> tuple[cidade]:
    res = list()

    with open(input_file, "r") as file:
        for line in file:
            nome, dist = line.split()
            c = cidade(nome, int(dist))
            res.append(c)

    return tuple(res)
        

def load_matrix(input_file: str) -> tuple[int]:
    matrix = list()

    with open(input_file, "r") as file:
        for line in file:
            matrix.append(tuple(line.split()))
    
    return tuple(matrix)

