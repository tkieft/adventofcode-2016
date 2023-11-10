import sys


def step(a: str) -> str:
    b = "".join(["1" if c == "0" else "0" for c in reversed(a)])
    return f"{a}0{b}"


def checksum(s: str) -> str:
    assert len(s) % 2 == 0
    result = ""
    for i in range(0, len(s), 2):
        result += "0" if s[i] != s[i + 1] else "1"
    return result


def day16(start: str, disk_length: int):
    s = start
    while True:
        s = step(s)
        if len(s) >= disk_length:
            break

    s = s[:disk_length]

    while len(s) % 2 == 0:
        s = checksum(s)

    print(s)


if __name__ == "__main__":
    day16(sys.argv[1], int(sys.argv[2]))
