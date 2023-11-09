import copy
import re
import sys


class Disc:
    i: int
    positions: int

    def __init__(self, positions: int, i: int):
        self.i = i
        self.positions = positions

    def __repr__(self):
        return f"{self.i}/{self.positions}"


def read_input(filename: str) -> list[Disc]:
    discs: list[Disc] = []
    search = re.compile(
        r"Disc #. has (\d+) positions; at time=0, it is at position (\d+).\w*"
    )
    with open(filename) as f:
        for line in f:
            if m := search.match(line):
                discs.append(Disc(int(m.group(1)), int(m.group(2))))

    return discs


def in_order(discs: list[Disc]):
    for i, disc in enumerate(discs):
        if (disc.i + i + 1) % disc.positions != 0:
            return False

    return True


def simulate(discs: list[Disc]) -> int:
    time = 0
    while True:
        if in_order(discs):
            return time
        time += 1
        for disc in discs:
            disc.i = disc.i + 1 % disc.positions


def day15(filename: str):
    discs = read_input(filename)
    print(simulate(copy.deepcopy(discs)))
    discs.append(Disc(11, 0))
    print(simulate(discs))


if __name__ == "__main__":
    day15(sys.argv[1])
