import copy
import itertools
import re
import sys

PATTERN = re.compile(r"(\w+)(-compatible)? (microchip|generator)")

def is_stable(items):
    generators = list(filter(lambda x: x[1] == "generator", items))
    unshielded_chips = list(filter(lambda x: (x[0], "generator") not in generators, items))
    return len(unshielded_chips) == 0 or len(generators) == 0

def pairwise_floors(current_floor, target_floor):
    assert current_floor != target_floor
    up = current_floor < target_floor
    floors = range(current_floor, target_floor) if up else reversed(range(target_floor + 1, current_floor + 1))
    for i in floors:
        yield (i, i + 1 if up else i - 1)

class BuildingState:
    FLOORS = 4

    def __init__(self):
        self.floors = [None for floor in range(BuildingState.FLOORS)]
        self.current_floor = 0
        self.total_moves = 0

    def __eq__(self, value):
        return self._canonical() == value._canonical()

    def __hash__(self):
        return hash(self._canonical())

    def __copy__(self):
        b = BuildingState()
        b.floors = [floor for floor in self.floors]
        b.current_floor = self.current_floor
        b.total_moves = self.total_moves
        return b

    def __str__(self):
        all_items = list(itertools.chain(*self.floors))
        all_items.sort(key = lambda x: x[0] + x[1])

        s = f"{self.total_moves} moves made\n" if self.total_moves >= 1 else "Start:\n"
        for i in reversed(range(4)):
            s += f"F{i + 1} "
            s += "E  " if self.current_floor == i else ".  "
            for j, chip in enumerate(all_items):
                if chip in self.floors[i]:
                    s += f"{chip[0][0:2].title()}{chip[1][0].upper()} "
                else:
                    s += ".   "
            s += "\n"
        return s

    def _canonical(self):
        compounds = frozenset(x[0] for floor in self.floors for x in floor)
        chip_to_floor = {x : i for i, floor in enumerate(self.floors) for x in floor}
        return (self.current_floor, tuple(sorted((chip_to_floor[(compound, "generator")], chip_to_floor[(compound, "microchip")]) for compound in compounds)))

    def items(self, floor = None):
        return self.floors[floor] if floor is not None else self.floors[self.current_floor]

    def at_top_floor(self):
        return self.current_floor == BuildingState.FLOORS - 1

    def at_bottom_floor(self):
        return self.current_floor == 0

    def empty_upto(self, floor):
        return not list(itertools.chain.from_iterable(self.floors[0:floor]))

    def can_add(self, floor, new_items):
        return is_stable(self.floors[floor].union(new_items))

    def can_remove(self, floor, old_items):
        return is_stable(self.floors[floor].difference(old_items))

    def can_transport(self, current_floor, target_floor, items):
        for (floor, next_floor) in pairwise_floors(current_floor, target_floor):
            if not self.can_remove(floor, items) or not self.can_add(next_floor, items):
                return False
        return True

    def move_items(self, current_floor, target_floor, items):
        for (floor, next_floor) in pairwise_floors(current_floor, target_floor):
            self.floors[floor] = self.floors[floor].difference(items)
            self.floors[next_floor] = self.floors[next_floor].union(items)
            self.current_floor = self.current_floor - 1 if current_floor > target_floor else self.current_floor + 1
            self.total_moves += 1

    def ready_for_assembly(self):
        return not self.floors[0] and not self.floors[1] and not self.floors[2]

def parse(filename):
    building = BuildingState()
    floor = 0
    with open(filename) as f:
        for line in f:
            matches = PATTERN.findall(line)
            building.floors[floor] = frozenset((match[0], match[2]) for match in matches)
            floor += 1

    return building

def day11(filename):
    visited = set()
    queue = [parse(filename)]
    queueset = set(queue)

    while queue:
        building = queue.pop(0)
        queueset.remove(building)
        visited.add(building)

        if building.ready_for_assembly():
            break

        for combo in itertools.chain(itertools.combinations(building.items(), 1), itertools.combinations(building.items(), 2)):
            if not building.at_top_floor() \
               and building.can_transport(building.current_floor, building.current_floor + 1, combo):
                new_building = copy.copy(building)
                new_building.move_items(building.current_floor, building.current_floor + 1, combo)
                if not new_building in visited and not new_building in queueset:
                    queue.append(new_building)
                    queueset.add(new_building)
            if not building.at_bottom_floor() \
               and not building.empty_upto(building.current_floor) \
               and building.can_transport(building.current_floor, building.current_floor - 1, combo):
                new_building = copy.copy(building)
                new_building.move_items(building.current_floor, building.current_floor - 1, combo)
                if not new_building in visited and not new_building in queueset:
                    queue.append(new_building)
                    queueset.add(new_building)

    print(f"Total steps: {building.total_moves}")
    print(f"Visited {len(visited)} nodes")


if __name__ == "__main__":
    day11(sys.argv[1])
