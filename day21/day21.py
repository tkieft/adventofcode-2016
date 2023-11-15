import re
import sys
from typing import Optional

SWAP_POSITION = re.compile(r"swap position (\d+) with position (\d+)")
SWAP_LETTER = re.compile(r"swap letter (.+) with letter (.+)")
ROTATE_STEPS = re.compile(r"rotate (left|right) (\d+) step(s)?")
ROTATE_POSITION = re.compile(r"rotate based on position of letter (.)")
REVERSE_POSITIONS = re.compile(r"reverse positions (\d+) through (\d+)")
MOVE_POSITION = re.compile(r"move position (\d+) to position (\d+)")


def execute_instruction(instruction: str, input: str, reverse: bool) -> str:
    s = list(input)

    if m := SWAP_POSITION.match(instruction):
        x, y = int(m.group(1)), int(m.group(2))
        s[x], s[y] = s[y], s[x]
    elif m := SWAP_LETTER.match(instruction):
        x, y = m.group(1), m.group(2)
        i, j = s.index(x), s.index(y)
        s[i], s[j] = y, x
    elif m := ROTATE_STEPS.match(instruction):
        dir, steps = m.group(1), int(m.group(2))
        if reverse:
            dir = "right" if dir == "left" else "left"
        if dir == "left":
            s = s[steps:] + s[:steps]
        else:
            s = s[-steps:] + s[:-steps]
    elif m := ROTATE_POSITION.match(instruction):
        x = m.group(1)
        i = s.index(x)

        if reverse:
            # abcdefgh
            # a (0) -> position 1
            # b (1) -> position 3
            # c (2) -> position 5
            # d (3) -> position 7
            # e (4) -> position 2
            # f (5) -> position 4
            # g (6) -> position 6
            # h (7) -> position 0 (8)
            if i % 2 == 1:
                steps = i - int(i / 2)
            else:
                original_position = len(s) - 1 if i == 0 else int((6 + i) / 2)
                steps = (i + len(s) - original_position) % len(s)
            # rotate left
            s = s[steps:] + s[:steps]
        else:
            steps = i + 1 + (1 if i >= 4 else 0)
            steps = steps % len(s)
            # rotate right
            s = s[-steps:] + s[:-steps]
    elif m := REVERSE_POSITIONS.match(instruction):
        x, y = int(m.group(1)), int(m.group(2))
        s[x : y + 1] = reversed(s[x : y + 1])
    elif m := MOVE_POSITION.match(instruction):
        x, y = int(m.group(1)), int(m.group(2))
        if reverse:
            x, y = y, x
        a = s[x]
        del s[x]
        s.insert(y, a)
    else:
        raise ValueError(f"Unrecognized instruction {instruction}")

    return "".join(s)


def day21(filename: str, password: str, scrambled: Optional[str] = None):
    with open(filename) as f:
        instructions = [line.strip() for line in f.readlines()]

    # Part 1
    res = password
    for i in instructions:
        res = execute_instruction(i, res, False)
    print(res)

    # Part 2
    if scrambled:
        res = scrambled
        for i in reversed(instructions):
            res = execute_instruction(i, res, True)

        print(res)


if __name__ == "__main__":
    day21(*sys.argv[1:])
