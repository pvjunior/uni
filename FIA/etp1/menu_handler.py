from load_cidades import *
from collections import deque
from heapq import heappop, heappush

matrix: tuple
heuristica: tuple
part: int
dest: int
algo: int


def start():
    global matrix, heuristica, part, dest, algo

    matrix = load_matrix("matrix.txt")
    heuristica = load_heuristica("heuristicas.txt")

    print("Partida:")
    _print_cidades()
    part = _read_choice("Escolha a cidade de partida: ", 0, len(heuristica) - 1)

    dest = 12

    _print_algoritmos()
    algo = _read_choice("Escolha o algoritmo: ", 1, 6)
    path = _run_algorithm(part, dest, algo)

    if path is None:
        print("Não foi encontrado um caminho.")
        return

    cidades = " -> ".join(heuristica[cidade].nome for cidade in path)
    custo = _path_cost(path)
    print(f"Caminho: {cidades}")
    print(f"Custo total: {custo}")


def _print_cidades():
    for i, c in enumerate(heuristica):
        print(f"[{i}] {c.nome}")


def _print_algoritmos():
    print("[1] Busca em largura (Breadth-first search)")
    print("[2] Busca em profundidade (Depth-first search)")
    print("[3] Busca de aprofundamento iterativo (Iterative Deepening Search)")
    print("[4] A* (A-estrela)")
    print("[5] Busca pela melhor escolha (Best-first search)")
    print("[6] Busca de custo uniforme (Uniform Cost Search)")


def _read_choice(prompt: str, minimum: int, maximum: int) -> int:
    while True:
        try:
            choice = int(input(prompt))
        except ValueError:
            print("Digite um número válido.")
            continue

        if minimum <= choice <= maximum:
            return choice

        print("Opção inválida.")


def _run_algorithm(start_node: int, goal_node: int, algorithm: int):
    algorithms = {
        1: breadth_first_search,
        2: depth_first_search,
        3: iterative_deepening_search,
        4: a_star_search,
        5: best_first_search,
        6: uniform_cost_search,
    }
    return algorithms[algorithm](start_node, goal_node)


def _neighbors(node: int):
    return (
        (neighbor, weight)
        for neighbor, weight in enumerate(matrix[node])
        if weight is not None and weight > 0
    )


def _reconstruct_path(parent: dict, goal_node: int):
    path = [goal_node]
    while path[-1] in parent:
        path.append(parent[path[-1]])
    return list(reversed(path))


def _path_cost(path: list) -> int:
    return sum(matrix[source][target] for source, target in zip(path, path[1:]))


def breadth_first_search(start_node: int, goal_node: int):
    frontier = deque([start_node])
    parent = {}
    visited = {start_node}

    while frontier:
        node = frontier.popleft()
        if node == goal_node:
            return _reconstruct_path(parent, goal_node)

        for neighbor, _ in _neighbors(node):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                frontier.append(neighbor)

    return None


def depth_first_search(start_node: int, goal_node: int):
    frontier = [start_node]
    parent = {}
    visited = {start_node}

    while frontier:
        node = frontier.pop()
        if node == goal_node:
            return _reconstruct_path(parent, goal_node)

        for neighbor, _ in reversed(tuple(_neighbors(node))):
            if neighbor not in visited:
                visited.add(neighbor)
                parent[neighbor] = node
                frontier.append(neighbor)

    return None


def iterative_deepening_search(start_node: int, goal_node: int):
    def depth_limited_search(node: int, limit: int, path: list):
        if node == goal_node:
            return path
        if limit == 0:
            return None

        for neighbor, _ in _neighbors(node):
            if neighbor not in path:
                result = depth_limited_search(neighbor, limit - 1, path + [neighbor])
                if result is not None:
                    return result
        return None

    for depth in range(len(matrix)):
        path = depth_limited_search(start_node, depth, [start_node])
        if path is not None:
            return path
    return None


def a_star_search(start_node: int, goal_node: int):
    frontier = []
    heappush(frontier, (_heuristic(start_node, goal_node), 0, start_node))
    parent = {}
    cost_so_far = {start_node: 0}

    while frontier:
        _, cost, node = heappop(frontier)
        if cost != cost_so_far[node]:
            continue
        if node == goal_node:
            return _reconstruct_path(parent, goal_node)

        for neighbor, weight in _neighbors(node):
            new_cost = cost + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = node
                heappush(
                    frontier,
                    (new_cost + _heuristic(neighbor, goal_node), new_cost, neighbor),
                )

    return None


def best_first_search(start_node: int, goal_node: int):
    frontier = []
    heappush(frontier, (_heuristic(start_node, goal_node), start_node))
    parent = {}
    visited = set()

    while frontier:
        _, node = heappop(frontier)
        if node in visited:
            continue
        visited.add(node)
        if node == goal_node:
            return _reconstruct_path(parent, goal_node)

        for neighbor, _ in _neighbors(node):
            if neighbor not in visited:
                parent[neighbor] = node
                heappush(frontier, (_heuristic(neighbor, goal_node), neighbor))

    return None


def uniform_cost_search(start_node: int, goal_node: int):
    frontier = [(0, start_node)]
    parent = {}
    cost_so_far = {start_node: 0}

    while frontier:
        cost, node = heappop(frontier)
        if cost != cost_so_far[node]:
            continue
        if node == goal_node:
            return _reconstruct_path(parent, goal_node)

        for neighbor, weight in _neighbors(node):
            new_cost = cost + weight
            if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                cost_so_far[neighbor] = new_cost
                parent[neighbor] = node
                heappush(frontier, (new_cost, neighbor))

    return None


def _heuristic(node: int, goal_node: int) -> int:
    return abs(heuristica[node].dist - heuristica[goal_node].dist)
