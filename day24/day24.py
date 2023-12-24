import itertools
import re
import sys

Board = list[str]
Coord = tuple[int, int]


def parse_input(filename: str):
    board: Board = []
    positions: dict[int, Coord] = {}
    digit_pattern = re.compile(r"\d")
    with open(filename) as f:
        while line := f.readline().strip():
            board += [line]
            for match in digit_pattern.finditer(line):
                positions[int(match[0])] = (match.start(), len(board) - 1)
    return board, positions


def neighbors(cur: Coord, board: Board) -> list[Coord]:
    neighbors = [
        n
        for n in [
            (cur[0] + 1, cur[1]),
            (cur[0] - 1, cur[1]),
            (cur[0], cur[1] + 1),
            (cur[0], cur[1] - 1),
        ]
        if n[0] in range(len(board[0]))
        and n[1] in range(len(board))
        and board[n[1]][n[0]] != "#"
    ]
    return neighbors


def find_path(a: Coord, b: Coord, board: Board) -> int:
    # Use dictionary as ordered set
    paths = [[a]]
    visited = {a}
    while paths:
        path = paths.pop(0)
        for n in neighbors(path[-1], board):
            if n == b:
                return len(path)
            if n in visited:
                continue
            visited.add(n)
            paths.append(path + [n])

    raise ValueError("No path found")


def path_length(paths: dict[tuple[int, int], int], path: tuple[int, ...]):
    current = 0
    cost = 0
    for node in path:
        cost += paths[(current, node)]
        current = node
    return cost


def day24(filename: str):
    board, positions = parse_input(filename)
    node_count = max(positions) + 1

    paths: dict[tuple[int, int], int] = {}

    # Calculate minimum path between all node pairs
    for a, b in itertools.combinations(range(node_count), 2):
        path = find_path(positions[a], positions[b], board)
        paths[(a, b)] = path
        paths[(b, a)] = path

    # Part 1
    min_path = sys.maxsize
    for path in itertools.permutations(range(1, node_count), node_count - 1):
        min_path = min(min_path, path_length(paths, path))
    print(min_path)

    # Part 2
    min_path = sys.maxsize
    for path in itertools.permutations(range(1, node_count), node_count - 1):
        min_path = min(min_path, path_length(paths, (*path, 0)))
    print(min_path)


if __name__ == "__main__":
    day24(sys.argv[1])
