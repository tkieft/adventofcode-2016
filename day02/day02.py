import sys

PART_1_TELEPHONE = [
    ['1', '2', '3'],
    ['4', '5', '6'],
    ['7', '8', '9']]

PART_2_TELEPHONE = [
  ['', '', '1', '', ''],
 ['', '2', '3', '4', ''],
['5', '6', '7', '8', '9'],
 ['', 'A', 'B', 'C', ''],
  ['', '', 'D', '', '']]
       
def move(telephone, char, x, y):
    newY = y
    newX = x
    
    if char == "U":
        newY = max(y - 1, 0)
    elif char == "D":
        newY = min(y + 1, len(telephone) - 1)
    elif char == "L":
        newX = max(x - 1, 0)
    elif char == "R":
        newX = min(x + 1, len(telephone[y]) - 1)

    return (newX, newY) if telephone[newY][newX] != '' else (x, y)

codes = open(sys.argv[1], 'r').readlines()

x = 1
y = 1
code = ''

for line in codes:
    for char in line.strip():
        x, y = move(PART_1_TELEPHONE, char, x, y)
        
    code += PART_1_TELEPHONE[y][x]

print(code)

x = 0
y = 2
code = ''

for line in codes:
    for char in line.strip():
        x, y = move(PART_2_TELEPHONE, char, x, y)

    code += PART_2_TELEPHONE[y][x]
print(code)