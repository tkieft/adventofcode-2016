import collections
import itertools
import re
import sys

HEIGHT = 6
WIDTH = 50

RECT_INST = re.compile(r"rect (\d+)x(\d+)")
ROTATE_ROW_INST = re.compile(r"rotate row y=(\d+) by (\d+)")
ROTATE_COL_INST = re.compile(r"rotate column x=(\d+) by (\d+)")

def _rotate(list, by):
    return list[len(list)-by:] + list[:len(list)-by]

class Screen:
    def __init__(self, width, height):
        self._width = width
        self._height = height
        self._pixels = [list("." * WIDTH) for i in range(HEIGHT)]

    def __str__(self):
        return "0....X....1....X....2....X....3....X....4....X....\n" + \
               "\n".join(''.join(row) for row in self._pixels)

    def pixels_on(self):
        return len(list(filter(lambda p: p == "#", itertools.chain.from_iterable(self._pixels))))

    def rect(self, width, height):
        for y in range(height):
            for x in range(width):
                self._pixels[y][x] = "#"

    def rotate_col(self, x, by):
        pixels = [row[x] for row in self._pixels]
        pixels = _rotate(pixels, by)
        for i, row in enumerate(self._pixels):
            row[x] = pixels[i]

    def rotate_row(self, y, by):
        self._pixels[y] = _rotate(self._pixels[y], by)


def day08(filename):
    screen = Screen(WIDTH, HEIGHT)

    with open(filename) as f:
        for instruction in f:
            m = RECT_INST.match(instruction)
            if m:
                screen.rect(int(m[1]), int(m[2]))
                continue
            m = ROTATE_ROW_INST.match(instruction)
            if m:
                screen.rotate_row(int(m[1]), int(m[2]))
                continue
            m = ROTATE_COL_INST.match(instruction)
            if m:
                screen.rotate_col(int(m[1]), int(m[2]))
                continue
    
    print(screen)
    print()
    print(screen.pixels_on())


if __name__ == "__main__":
    day08(sys.argv[1])
