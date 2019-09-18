import sys

def grid_distance(location):
    return abs(location[0]) + abs(location[1])

input = open(sys.argv[1], 'r').readlines()[0]
directions = input.split(", ")

heading = 90
current = (0, 0)
headquarters = None

visited = []
visited.append(current)

for direction in directions:
    # Turn in new direction
    heading += -90 if direction[0] == "R" else 90
    heading %= 360

    # Walk
    steps = int(direction[1:])
    for i in range(steps):
        delta = 1 if heading <= 90 else -1
        current = (
            current[0] + (delta if heading % 180 == 90 else 0),
            current[1] + (delta if heading % 180 == 0 else 0)
        )

        if headquarters == None and current in visited:
            headquarters = current
        else:
            visited.append(current)

print(grid_distance(current))
print(grid_distance(headquarters))
