from collections import defaultdict
import pprint
import re
import sys

VALUE_INST = re.compile(r"value (\d+) goes to bot (\d+)")
GIVE_INST = re.compile(r"bot (\d+) gives low to (\w+) (\d+) and high to (\w+) (\d+)")

class Bot:
    def __init__(self):
        self._chips = []
        self.low = None
        self.high = None

    def __len__(self):
        return len(self._chips)

    def __str__(self):
        return f"Bot holding [{', '.join(map(str, self._chips))}]"

    __repr__ = __str__

    def add_chip(self, chip):
        self._chips.append(chip)
        assert len(self._chips) <= 2

    def go(self):
        self.high.add_chip(max(self._chips))
        self.low.add_chip(min(self._chips))
        chipsgiven = tuple(self._chips)
        self._chips = []
        return chipsgiven

class Output:
    def __init__(self):
        self._value = None

    def __str__(self):
        return f"Output holding {self._value}"

    __repr__ = __str__

    def add_chip(self, chip):
        assert self._value is None
        self._value = chip

    def value(self):
        return self._value


def parse_file(filename):
    bots = defaultdict(Bot)
    outputs = defaultdict(Output)

    with open(filename) as f:
        for line in f:
            if line.startswith("value"):
                m = VALUE_INST.match(line)
                bot = bots[int(m[2])]
                bot.add_chip(int(m[1]))
            else:
                m = GIVE_INST.match(line)
                bot = bots[int(m[1])]
                bot.low = outputs[int(m[3])] if m[2] == "output" else bots[int(m[3])]
                bot.high = outputs[int(m[5])] if m[4] == "output" else bots[int(m[5])]

    return bots, outputs

def day10(filename):
    bots, outputs = parse_file(filename)

    while True:
        bots2 = {key: bot for key, bot in bots.items() if len(bot) == 2}
        if not bots2:
            break
        for key, bot in bots2.items():
            chipsgiven = bot.go()
            if 61 in chipsgiven and 17 in chipsgiven:
                print(key)

    print(outputs[0].value() * outputs[1].value() * outputs[2].value())

if __name__ == "__main__":
    day10(sys.argv[1])
