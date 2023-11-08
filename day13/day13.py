import sys
from enum import Enum, unique

Coord = tuple[int, int]


@unique
class Square(Enum):
    OPEN = 0
    WALL = 1


SQUARES: dict[Coord, Square] = {}


def square(coord: Coord, favorite: int) -> Square:
    if coord not in SQUARES:
        (x, y) = coord
        sum = x * x + 3 * x + 2 * x * y + y + y * y + favorite
        SQUARES[coord] = Square(bin(sum).count("1") % 2)
    return SQUARES[coord]


def day13(favorite: int, target: Coord):
    start = (1, 1)
    paths: list[list[Coord]] = [[start]]

    target_distance = 0
    visited: set[Coord] = set([start])

    while target_distance == 0:
        path = paths.pop(0)
        cur = path[-1]
        for next in [
            (cur[0] - 1, cur[1]),
            (cur[0] + 1, cur[1]),
            (cur[0], cur[1] - 1),
            (cur[0], cur[1] + 1),
        ]:
            if next[0] < 0 or next[1] < 0:
                continue
            if target_distance == 0 and next == target:
                target_distance = len(path)
            if next not in path and square(next, favorite) == Square.OPEN:
                paths.append(path + [next])
                if len(path) <= 50:
                    visited.add(next)

    print(target_distance)
    print(len(visited))


if __name__ == "__main__":
    ints = [int(x) for x in sys.argv[1:]]
    day13(ints[0], (ints[1], ints[2]))
