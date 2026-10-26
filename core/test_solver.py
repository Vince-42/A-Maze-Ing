from core.maz_solver import MazSolver


class FakeCell:
    def __init__(self, x, y, value):
        self.coordinate = (x, y)
        self.stateN = not bool(value & 1)
        self.stateE = not bool(value & 2)
        self.stateS = not bool(value & 4)
        self.stateW = not bool(value & 8)
        self.fortytwo = False


with open("test_maze.txt") as f:
    lines = f.read().strip().splitlines()

maze_data = lines[:-3]

cells = []

for y, row in enumerate(maze_data):
    for x, char in enumerate(row):
        value = int(char, 16)
        cells.append(FakeCell(x, y, value))

entry = (0, 0)
exit = (9, 13)

solver = MazSolver(cells, entry, exit)

# print("Entry neighbors:", solver.get_neighbors(entry))
# print("Exit neighbors:", solver.get_neighbors(exit))
# print("Solution:", solver.solve())

path = solver.solve()

print("Shortest path:", path)
print("Path found:", bool(path))

if path:
    print("Path length:", len(path) - 1)
    print("Start:", path[0])
    print("End:", path[-1])