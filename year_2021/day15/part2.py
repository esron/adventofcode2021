from decimal import Decimal
from sys import path, stdin
from typing import Iterable
from queue import PriorityQueue

class Point:
    def __init__(self, coord: 'tuple[int, int]', value: int) -> None:
        self.x = coord[0]
        self.y = coord[1]
        self.value = value
        self.f = Decimal('Infinity')
        self.g = Decimal('Infinity')
        self.father: Point = None

    def distance(self, point: 'Point') -> int:
        """Manhattan distance to point"""
        return (point.x - self.x) + (point.y - self.y)

    def set_father(self, point: 'Point') -> None:
        self.father = point

    def __eq__(self, __o: object) -> bool:
        if isinstance(__o, Point):
            return self.x == __o.x and self.y == __o.y
        else:
            return False

    def __gt__(self, __o: object) -> bool:
        return self.f > __o.f

    def __lt__(self, __o: object) -> bool:
        return self.f < __o.f

    def __hash__(self) -> int:
        return hash((self.x, self.y))

    def __str__(self) -> str:
        return f'{{ x: {str(self.x)}, y: {str(self.y)}, f: {self.f}, \
g: {self.g} value: {self.value} }}'

def is_in_range(x: int, y: int, grid: Iterable[Iterable[int]]) -> bool:
    return (0 <= x < len(grid)) and (0 <= y < len(grid[x]))

def append_if_in_range(grid, n, direction):
    if is_in_range(*direction, grid):
        n.append(grid[direction[0]][direction[1]])

def get_neighbors(point: Point, grid: Iterable[Iterable[int]]) -> Iterable[Point]:
    n = []

    append_if_in_range(grid, n, (point.x - 1, point.y))
    append_if_in_range(grid, n, (point.x, point.y - 1))
    append_if_in_range(grid, n, (point.x + 1, point.y))
    append_if_in_range(grid, n, (point.x, point.y + 1))

    return n

def pathfinder(A: Point, goal: Point, grid: Iterable[Iterable[int]]) -> Point:
    open_list = PriorityQueue()
    open_list.put(A)
    closed_list = set()
    i = 1
    while not open_list.empty():
        if i % 1000 == 0:
            print('Iteration: ', i)
        i += 1
        current: Point = open_list.get()
        closed_list.add(current)
        if current == goal:
            return current

        neighbors = get_neighbors(current, grid)

        for n in neighbors:
            if n in closed_list:
                continue

            new_g = current.g + n.value

            if new_g < n.g:
                n.father = current
                n.g = new_g
                n.f = new_g + n.distance(goal)
                open_list.put(n)

def increment(x: int) -> int:
    return x % 9 + 1

grid = []
f = open('day15.txt')
for line in f:
    l = list(map(int, line.rstrip()))
    ll = l.copy()
    for _ in range(4):
        l = list(map(increment, l))
        ll += l

    grid.append(ll)

g = grid.copy()
for _ in range(4):
    for i in range(len(g)):
        g[i] = list(map(increment, g[i]))

    grid += g

for i in range(len(grid)):
    for j in range(len(grid[i])):
        grid[i][j] = Point((i, j), grid[i][j])

start = grid[0][0]
start.g = 0
start.f = 0
goal  = grid[len(grid) - 1][len(grid[0]) - 1]

point = pathfinder(start, goal, grid)

print(point.f)