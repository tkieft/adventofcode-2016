from __future__ import annotations

import sys
from dataclasses import dataclass


@dataclass
class Elf:
    id: int
    presents: int


class Node:
    elf: Elf
    prev: Node
    next: Node


def part1(elves: int) -> int:
    arr = [Elf(i + 1, 1) for i in range(elves)]
    while len(arr) > 1:
        new_arr = []
        for i, elf in enumerate(arr):
            if elf.presents != 0:
                tgt_elf = new_arr[0] if i == len(arr) - 1 else arr[i + 1]
                elf.presents += tgt_elf.presents
                tgt_elf.presents = 0
                new_arr.append(elf)

        arr = new_arr

    return arr[0].id


def make_list(elves: int) -> Node:
    elf = Elf(1, 1)
    start = Node()
    start.elf = elf

    prev = start
    for i in range(1, elves):
        elf = Elf(i + 1, 1)
        node = Node()
        node.elf = elf
        prev.next = node
        node.prev = prev
        prev = node

    prev.next = start
    start.prev = prev

    return start


def find_mid(start: Node, elves: int) -> Node:
    mid = start
    for _ in range(int(elves / 2)):
        mid = mid.next
    return mid


def part2(elves: int) -> int:
    cur = make_list(elves)
    opp = find_mid(cur, elves)

    while cur.next != cur:
        cur.elf.presents += opp.elf.presents
        opp.prev.next = opp.next
        opp.next.prev = opp.prev
        elves -= 1

        cur = cur.next
        opp = opp.next
        if elves % 2 == 0:
            opp = opp.next

    return cur.elf.id


def day19(elves: int):
    print(part1(elves))
    print(part2(elves))


if __name__ == "__main__":
    day19(int(sys.argv[1]))
