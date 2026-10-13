from load_cidades import *

matrix = tuple()
heuristica = tuple()

def start():
    matrix = load_matrix("matrix.txt")
    heuristica = load_heuristica("heuristicas.txt")

    print("aa")
    print("Partida: ")
    _print_cidades()
   
def _print_cidades():
    print(heuristica)
    for i, c in enumerate(heuristica):
        print(f"{i} - {c.nome}")



