import re
import sys

PATTERN = re.compile(r"(\d+)x(\d+)")

def decompress(data, recursive=False):
    length = 0
    i = 0
    while i < len(data):
        c = data[i]
        i += 1

        if c != "(":
            length += 1
            continue

        # Found marker            
        match = PATTERN.match(data, i)
        num_chars = int(match[1])
        num_repeats = int(match[2])
        i += len(match[0]) + 1
        length += num_repeats * (decompress(data[i:i + num_chars], True) if recursive else num_chars)
        i += num_chars

    return length

def day09(filename):
    with open(filename) as f:
        data = f.read()

    print(decompress(data))
    print(decompress(data, True))

if __name__ == "__main__":
    day09(sys.argv[1])