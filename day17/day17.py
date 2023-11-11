import sys
from hashlib import md5

Coord = tuple[int, int]


def possible_exits(coord: Coord) -> dict[str, Coord]:
    possible_x: list[tuple[int, str]] = [
        x for x in [(coord[0] + 1, "R"), (coord[0] - 1, "L")] if x[0] in range(0, 4)
    ]
    possible_y: list[tuple[int, str]] = [
        y for y in [(coord[1] + 1, "D"), (coord[1] - 1, "U")] if y[0] in range(0, 4)
    ]
    return {x[1]: (x[0], coord[1]) for x in possible_x} | {
        y[1]: (coord[0], y[0]) for y in possible_y
    }


def find_paths(passcode: str) -> list[str]:
    working_paths: list[tuple[Coord, str]] = [((0, 0), "")]
    complete_paths: list[str] = []

    while working_paths:
        coord, path = working_paths.pop(0)
        hash = md5(bytes(passcode + path, "utf8")).hexdigest()
        exits = possible_exits(coord)
        for i, dir in enumerate(("U", "D", "L", "R")):
            if dir in exits and hash[i] in "bcdef":
                new_path = path + dir
                if exits[dir] == (3, 3):
                    complete_paths.append(new_path)
                else:
                    working_paths.append((exits[dir], new_path))

    return complete_paths


def day17(passcode: str):
    paths = find_paths(passcode)
    print(paths[0])
    print(len(paths[-1]))


if __name__ == "__main__":
    day17(sys.argv[1])
