import itertools
import re
import sys

FORMAT = re.compile(r"(.*?)-(\d+)\[(\w+)\]")

def parse_room(line):
    result = FORMAT.match(line)
    return (result[1], int(result[2]), result[3])
    
def is_real(room):
    letters = sorted(room[0].replace("-", ""))
    letter_counts = [(l[0], len(tuple(l[1]))) for l in itertools.groupby(letters)]
    letter_counts.sort(key=lambda x: x[1], reverse=True)

    for i in range(5):
        if letter_counts[i][0] not in room[2]:
            return False
    return True

def shift(letter, by):
    return chr((ord(letter) + by - ord('a')) % 26 + ord('a'))

def decrypt(room):
    return ''.join(map(lambda l: " " if l == "-" else shift(l, room[1]), room[0]))

def day04(filename):
    with open(filename) as f:
        rooms = [parse_room(line) for line in f if line]

    # Part 1
    rooms = list(filter(is_real, rooms))
    sector_id_sum = sum(map(lambda x: x[1], rooms))
    print(sector_id_sum)

    # Part 2
    northpole_storage = next(room for room in rooms if decrypt(room) == "northpole object storage")
    print(northpole_storage[1])


if __name__ == "__main__":
    day04(sys.argv[1])