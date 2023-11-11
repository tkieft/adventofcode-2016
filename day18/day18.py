import sys

TRAP_PATTERNS = ["^^.", ".^^", "^..", "..^"]


def count_safe_tiles(start: str, rows: int):
    safe_tiles = start.count(".")
    line = start
    for i in range(rows - 1):
        new_line = ""

        for i, c in enumerate(line):
            l = "." if i == 0 else line[i - 1]
            r = "." if i == len(line) - 1 else line[i + 1]
            new_line = new_line + ("^" if f"{l}{c}{r}" in TRAP_PATTERNS else ".")

        safe_tiles += new_line.count(".")
        line = new_line

    return safe_tiles


def day18(filename: str):
    with open(filename) as f:
        line = f.readline().strip()

    print(count_safe_tiles(line, 40))
    print(count_safe_tiles(line, 400_000))


if __name__ == "__main__":
    day18(sys.argv[1])
