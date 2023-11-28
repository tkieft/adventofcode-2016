import itertools
import re
import sys
from dataclasses import dataclass


@dataclass
class Node:
    x: int
    y: int
    size: int
    used: int
    avail: int


Coord = tuple[int, int]
NodeDict = dict[Coord, Node]


def parse_input(filename: str):
    nodes: NodeDict = {}
    pattern = re.compile(
        r"/dev/grid/node-x(\d+)-y(\d+)\s+(\d+)T\s+(\d+)T\s+(\d+)T\s+(\d+)%"
    )
    with open(filename) as f:
        for line in f:
            line = line.strip()
            if match := pattern.match(line):
                x = int(match[1])
                y = int(match[2])
                nodes[(x, y)] = Node(
                    x,
                    y,
                    int(match[3]),
                    int(match[4]),
                    int(match[5]),
                )

    return nodes


def part1(nodes: NodeDict):
    count = 0
    for a, b in itertools.permutations(nodes.values(), 2):
        if a.used > 0 and a.used <= b.avail:
            count += 1
    return count


def traverse(
    nodes: NodeDict, start: Coord, end: Coord, max: Coord, exclude: list[Coord] = []
):
    paths: list[list[Coord]] = [[start]]
    visited = {start}

    while paths:
        path = paths.pop(0)
        cur = path[-1]

        if cur == end:
            return len(path) - 1
        else:
            adjacent_coords = [
                (cur[0] - 1, cur[1]),
                (cur[0], cur[1] - 1),
                (cur[0] + 1, cur[1]),
                (cur[0], cur[1] + 1),
            ]
            for coord in adjacent_coords:
                if (
                    coord not in visited
                    and coord not in exclude
                    and coord[0] in range(0, max[0] + 1)
                    and coord[1] in range(0, max[1] + 1)
                    and nodes[coord].used <= nodes[cur].size
                ):
                    paths += [path + [coord]]
                    visited.add(coord)

    raise ValueError


def part2(nodes: NodeDict):
    max_x = max(a[0] for a in nodes)
    max_y = max(a[1] for a in nodes)
    goal = (max_x, 0)
    empty_node = [node for node in nodes.values() if node.used == 0][0]

    # Move the free node to an adjacent node
    path_steps = traverse(nodes, (empty_node.x, empty_node.y), goal, (max_x, max_y)) - 1

    # Move the data to the free node
    path_steps += 1

    for x in range(max_x - 1, 0, -1):
        # Move the free node around the data
        path_steps += traverse(
            nodes, (x + 1, 0), (x - 1, 0), (max_x, max_y), exclude=[(x, 0)]
        )
        # Move the data
        path_steps += 1

    return path_steps


def day22(filename: str):
    nodes = parse_input(filename)
    print(part1(nodes))
    print(part2(nodes))


if __name__ == "__main__":
    day22(sys.argv[1])
