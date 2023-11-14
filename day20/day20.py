import sys


def collapse_ranges(ranges: list[range]) -> list[range]:
    ranges.sort(key=lambda r: r.start)
    res: list[range] = []

    cur = ranges[0]
    for r in ranges[1:]:
        if cur.stop >= r.start:
            if cur.stop < r.stop:
                cur = range(cur.start, r.stop)
        else:
            res.append(cur)
            cur = r

    res.append(cur)
    return res


def day20(filename: str):
    ranges: list[range] = []
    with open(filename) as f:
        while line := f.readline().strip():
            parts = [int(n) for n in line.split("-")]
            ranges.append(range(parts[0], parts[1] + 1))

    ranges = collapse_ranges(ranges)

    # Part 1
    print(ranges[0].stop)

    # Part 2
    print(4294967295 - sum(r.stop - r.start for r in ranges) + 1)


if __name__ == "__main__":
    day20(sys.argv[1])
