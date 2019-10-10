import sys

def isValidTriangle(triangle):
    return (triangle[0] + triangle[1] > triangle[2] and
        triangle[1] + triangle[2] > triangle[0] and
        triangle[0] + triangle[2] > triangle[1])

triangles = [tuple([int(j) for j in  x.split()]) for x in open(sys.argv[1], 'r').readlines()]

# Part 1

print(sum([isValidTriangle(t) for t in triangles]))

# Part 2

goodTriangles = 0

for i in range(int(len(triangles) / 3)):
    for j in range(3):
        if isValidTriangle((triangles[i * 3][j], triangles[i * 3 + 1][j], triangles[i * 3 + 2][j])):
            goodTriangles += 1

print(goodTriangles)