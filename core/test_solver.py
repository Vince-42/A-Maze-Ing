from core.maz_solver import MazSolver


class FakeCell:
    def __init__(self, x, y, value):
        self.coordinate = (x, y)
        self.stateN = bool(value & 1)
        self.stateE = bool(value & 2)
        self.stateS = bool(value & 4)
        self.stateW = bool(value & 8)
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

print("Entry neighbors:", solver.get_neighbors(entry))
print("Exit neighbors:", solver.get_neighbors(exit))
print("Solution:", solver.solve())